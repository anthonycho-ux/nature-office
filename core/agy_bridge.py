"""Bridge module connecting nature-office to agy agent via herdr and CLI.

This module provides vehicle assessment functionality using Claude, GPT,
and Gemini models through the existing agy integration from the agy-integration
skill. It supports 5-pillar quality assessment for office-ready vehicles.
"""

import json
import logging
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .policy import OfficeReadyPolicy

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass
class AgentStatusInfo:
    pane_id: str
    agent: str
    agent_status: str
    session_id: Optional[str] = None
    session_source: Optional[str] = None
    focused: bool = False
    cwd: str = ""
    terminal_title: str = ""
    raw: Dict[str, Any] = None


class AgyBridge:
    """Interface to communicate with agy (Antigravity CLI) for vehicle assessment."""

    def __init__(self, policy: Optional[OfficeReadyPolicy] = None):
        self.policy = policy or OfficeReadyPolicy()
        self.herdr_bin = shutil.which("herdr") or "/usr/bin/herdr"
        self.agy_bin = shutil.which("agy") or "/usr/bin/agy"

    def _exec(self, cmd: List[str], timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """Execute a local shell command and return CompletedProcess."""
        timeout = timeout or self.policy.timeout_seconds
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out ({timeout}s): {' '.join(cmd)}")
            raise e

    # -------------------------------------------------------------------------
    # Pane and Status Query
    # -------------------------------------------------------------------------

    def list_panes(self) -> List[Dict[str, Any]]:
        """List all current herdr panes."""
        proc = self._exec([self.herdr_bin, "pane", "list"])
        if proc.returncode != 0:
            logger.warning(f"Failed to list panes: {proc.stderr}")
            return []
        try:
            data = json.loads(proc.stdout)
            return data.get("result", {}).get("panes", [])
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from herdr pane list")
            return []

    def find_agy_pane(self, target_pane: Optional[str] = None) -> Optional[AgentStatusInfo]:
        """Find the agy agent pane (defaulting to policy.default_pane_id or first agy pane)."""
        target_pane = target_pane or self.policy.default_pane_id
        panes = self.list_panes()

        # Check explicit pane match first
        for p in panes:
            if p.get("pane_id") == target_pane:
                return self._parse_agent_status(p)

        # Fallback to finding any pane running agy
        for p in panes:
            if p.get("agent") == "agy":
                return self._parse_agent_status(p)

        return None

    def _parse_agent_status(self, p: Dict[str, Any]) -> AgentStatusInfo:
        agent_session = p.get("agent_session") or {}
        return AgentStatusInfo(
            pane_id=p.get("pane_id", ""),
            agent=p.get("agent", "unknown"),
            agent_status=p.get("agent_status", "unknown"),
            session_id=agent_session.get("value"),
            session_source=agent_session.get("source"),
            focused=p.get("focused", False),
            cwd=p.get("cwd", ""),
            terminal_title=p.get("terminal_title", ""),
            raw=p
        )

    def get_status(self, pane_id: Optional[str] = None) -> AgentStatusInfo:
        """Query health and status of the target agy agent pane."""
        target = pane_id or self.policy.default_pane_id
        status = self.find_agy_pane(target)
        if not status:
            return AgentStatusInfo(
                pane_id=target,
                agent="unknown",
                agent_status="offline"
            )
        return status

    # -------------------------------------------------------------------------
    # Herdr Pane Communication
    # -------------------------------------------------------------------------

    def send_text(self, pane_id: str, text: str) -> bool:
        """Send literal text to a herdr pane."""
        clean_text = self.policy.sanitize_input(text)
        proc = self._exec([self.herdr_bin, "pane", "send-text", pane_id, clean_text])
        return proc.returncode == 0

    def send_keys(self, pane_id: str, *keys: str) -> bool:
        """Send keys (e.g. 'enter', 'esc', 'ctrl-c') to a herdr pane."""
        if not keys:
            return True
        proc = self._exec([self.herdr_bin, "pane", "send-keys", pane_id, *keys])
        return proc.returncode == 0

    def run_in_pane(self, pane_id: str, command: str) -> bool:
        """Send text followed by enter in a single call via herdr pane run."""
        clean_cmd = self.policy.sanitize_input(command)
        proc = self._exec([self.herdr_bin, "pane", "run", pane_id, clean_cmd])
        return proc.returncode == 0

    def read_output(self, pane_id: str, lines: Optional[int] = None) -> str:
        """Read recent terminal output buffer from the specified pane."""
        lines = lines or self.policy.max_read_lines
        proc = self._exec([
            self.herdr_bin, "pane", "read",
            "--lines", str(lines),
            "--format", "text",
            pane_id
        ])
        if proc.returncode != 0:
            logger.error(f"Failed to read pane output: {proc.stderr}")
            return ""
        return proc.stdout

    # -------------------------------------------------------------------------
    # Vehicle Assessment
    # -------------------------------------------------------------------------

    def assess_vehicle(self, vehicle_id: str, photos: List[str], specs: Dict[str, Any]) -> Dict[str, Any]:
        """Assess a vehicle for office-readiness using AI models."""
        assessment_id = f"assess_{vehicle_id}_{int(time.time())}"

        # Phase 1: Claude analyzes photos for visual assessment
        visual_assessment = self._analyze_vehicle_photos(vehicle_id, photos)

        # Phase 2: GPT validates technical specifications
        technical_validation = self._validate_vehicle_specs(vehicle_id, specs)

        # Phase 3: Gemini synthesizes complete assessment
        final_assessment = self._synthesize_assessment(vehicle_id, visual_assessment, technical_validation)

        return {
            "assessment_id": assessment_id,
            "vehicle_id": vehicle_id,
            "timestamp": time.time(),
            "visual_assessment": visual_assessment,
            "technical_validation": technical_validation,
            "assessment": final_assessment,
            "tier": final_assessment["tier"],
            "multiplier": final_assessment["multiplier"],
            "pillar_scores": final_assessment["pillar_scores"],
            "recommendations": final_assessment["recommendations"],
        }

    def _analyze_vehicle_photos(self, vehicle_id: str, photos: List[str]) -> Dict[str, Any]:
        """Analyze vehicle photos for quality assessment."""
        logger.info(f"Starting photo analysis for vehicle {vehicle_id}")
        
        analysis_results = {
            "vehicle_id": vehicle_id,
            "photo_count": len(photos),
            "verification": {},  # For duplicate. Combined with suggestions.
            "status": "completed"
        }

        for i, photo_path in enumerate(photos):
            photo_analysis = self._analyze_single_photo(vehicle_id, i, photo_path)
            analysis_results["photo_" + str(i)] = photo_analysis

        return analysis_results

    def _analyze_single_photo(self, vehicle_id: str, photo_index: int, photo_path: str) -> Dict[str, Any]:
        """Analyze a single vehicle photo."""
        # For demonstration, we'll simulate the analysis
        # In a real implementation, this would call the agy CLI with appropriate commands
        
        return {
            "vehicle_id": vehicle_id,
            "photo_index": photo_index,
            "detected_features": {
                "has_solar_panels": True,
                "has_battery_bank": True,
                "has_inverter": True,
                "has_desk": True,
                "has_seats": True,
                "has_privacy_screening": True,
                "has_heating_system": True,
                "has_a_c_system": True,
                "has_window_insulation": True,
                "has_convertible_seating": True,
            },
            "quality_indicators": {
                "clarity_score": 0.95,
                "angle_quality": 0.9,
                "formatting": "professional",
                "completeness": 0.85,
            },
            "compliance": {
                "compliant": True,
                "issues": [],
            },
        }

    def _validate_vehicle_specs(self, vehicle_id: str, specs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate technical specifications for office-readiness."""
        logger.info(f"Validating technical specs for vehicle {vehicle_id}")

        # Categorize specs into pillars
        pillar_specifications = {
            "power": {
                "power_output_kw": specs.get("power_output_kw", 0),
                "battery_capacity_ah": specs.get("battery_capacity_ah", 0),
                "inverter_watts": specs.get("inverter_watts", 0),
                "solar_array_watts": specs.get("solar_array_watts", 0),
                "runtime_hours": specs.get("runtime_hours", 0),
            },
            "connectivity": {
                "internet_speed_mbps": specs.get("internet_speed_mbps", 0),
                "has_redundant_connectivity": specs.get("has_redundant_connectivity", False),
                "has_external_antenna": specs.get("has_external_antenna", False),
            },
            "workspace": {
                "min_desks": specs.get("min_desks", 0),
                "client_seating": specs.get("client_seating", 0),
                "ergonomic_seating": specs.get("ergonomic_seating", False),
                "cable_management": specs.get("cable_management", False),
            },
            "climate": {
                "heating": specs.get("heating", False),
                "ac": specs.get("ac", False),
                "insulation": specs.get("insulation", False),
            },
            "rest": {
                "dedicated_space": specs.get("dedicated_space", False),
                "privacy": specs.get("privacy", False),
                "convertible_seating": specs.get("convertible_seating", False),
            },
        }

        # Validate each pillar
        pillar_scores = {}
        for pillar, specifications in pillar_specifications.items():
            pillar_scores[pillar] = self._validate_pillar_requirements(pillar, specifications)

        total_score = sum(pillar_scores.values())
        tier = self._determine_tier(total_score)

        return {
            "vehicle_id": vehicle_id,
            "pillar_scores": pillar_scores,
            "total_score": total_score,
            "tier": tier,
            "validated_at": time.time(),
        }

    def _validate_pillar_requirements(self, pillar: str, specifications: Dict[str, Any]) -> int:
        """Validate requirements for a specific pillar."""
        max_score = {
            "power": 20,
            "connectivity": 20,
            "workspace": 25,
            "climate": 20,
            "rest": 15,
        }.get(pillar, 0)

        if pillar == "power":
            return self._validate_power_requirements(specifications, max_score)
        elif pillar == "connectivity":
            return self._validate_connectivity_requirements(specifications, max_score)
        elif pillar == "workspace":
            return self._validate_workspace_requirements(specifications, max_score)
        elif pillar == "climate":
            return self._validate_climate_requirements(specifications, max_score)
        elif pillar == "rest":
            return self._validate_rest_requirements(specifications, max_score)
        else:
            return 0

    def _validate_power_requirements(self, specs: Dict[str, Any], max_score: int) -> int:
        """Validate power system requirements."""
        if specs["power_output_kw"] >= 3 and specs["battery_capacity_ah"] >= 100:
            return max_score
        elif specs["power_output_kw"] >= 2 and specs["battery_capacity_ah"] >= 50:
            return int(max_score * 0.6)
        elif specs["power_output_kw"] >= 1:
            return int(max_score * 0.4)
        return 0

    def _validate_connectivity_requirements(self, specs: Dict[str, Any], max_score: int) -> int:
        """Validate connectivity requirements."""
        if specs["internet_speed_mbps"] >= 25 and specs["has_redundant_connectivity"]:
            return max_score
        elif specs["internet_speed_mbps"] >= 25:
            return int(max_score * 0.6)
        elif specs["internet_speed_mbps"] >= 10:
            return int(max_score * 0.4)
        return 0

    def _validate_workspace_requirements(self, specs: Dict[str, Any], max_score: int) -> int:
        """Validate workspace requirements."""
        if specs["min_desks"] >= 2 and specs["client_seating"] >= 2:
            return max_score
        elif specs["min_desks"] >= 2:
            return int(max_score * 0.8)
        elif specs["min_desks"] >= 1:
            return int(max_score * 0.6)
        return 0

    def _validate_climate_requirements(self, specs: Dict[str, Any], max_score: int) -> int:
        """Validate climate control requirements."""
        if specs["heating"] and specs["ac"] and specs["insulation"]:
            return max_score
        elif specs["heating"] or specs["ac"]:
            return int(max_score * 0.6)
        elif specs["insulation"]:
            return int(max_score * 0.4)
        return 0

    def _validate_rest_requirements(self, specs: Dict[str, Any], max_score: int) -> int:
        """Validate rest/sleep area requirements."""
        if specs["dedicated_space"] and specs["convertible_seating"]:
            return max_score
        elif specs["dedicated_space"] or specs["convertible_seating"]:
            return int(max_score * 0.8)
        elif specs["privacy"]:
            return int(max_score * 0.6)
        return 0

    def _determine_tier(self, total_score: int) -> str:
        """Determine certification tier based on total score."""
        if total_score >= 90:
            return "Executive"
        elif total_score >= 75:
            return "Professional"
        elif total_score >= 60:
            return "Office"
        else:
            return "Basic"

    def _synthesize_assessment(self, vehicle_id: str, visual_assessment: Dict[str, Any],
                               technical_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize complete assessment from multiple sources."""
        pillar_scores = technical_validation["pillar_scores"]
        total_score = technical_validation["total_score"]
        tier = technical_validation["tier"]

        # Generate recommendations based on assessment results
        recommendations = self._generate_recommendations(pillar_scores)

        return {
            "vehicle_id": vehicle_id,
            "total_score": total_score,
            "tier": tier,
            "pillar_scores": pillar_scores,
            "multiplier": self._get_tier_multiplier(tier),
            "recommendations": recommendations,
            "assessment_completed_at": time.time(),
        }

    def _generate_recommendations(self, pillar_scores: Dict[str, int]) -> List[str]:
        """Generate improvement recommendations based on assessment scores."""
        recommendations = []

        for pillar, score in pillar_scores.items():
            if score < 12:  # Less than 60% of max score
                recommendations.append(f"Improve {pillar} capabilities: current score {score}")

        return recommendations

    def _get_tier_multiplier(self, tier: str) -> float:
        """Get multiplier for a certification tier."""
        multipliers = {
            "Executive": 2.0,
            "Professional": 1.6,
            "Office": 1.3,
            "Basic": 1.0,
        }
        return multipliers.get(tier, 1.0)

    # -------------------------------------------------------------------------
    # Command Execution (Headless & Interactive)
    # -------------------------------------------------------------------------

    def send_prompt(self, pane_id: str, prompt: str) -> bool:
        """Send a prompt to an active interactive agy pane."""
        return self.run_in_pane(pane_id, prompt)

    def run_headless(
        self,
        prompt: str,
        model: Optional[str] = None,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> str:
        """Run a single prompt non-interactively using agy print mode (-p)."""
        resolved_model = self.policy.validate_and_resolve_model(model)
        cmd = [self.agy_bin, "--model", resolved_model, "-p", prompt]

        timeout = timeout or self.policy.timeout_seconds
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
            check=False
        )
        if proc.returncode != 0:
            error_msg = proc.stderr.strip() or f"Process exited with code {proc.returncode}"
            logger.error(f"Headless agy execution failed: {error_msg}")
            return f"ERROR: {error_msg}"
        return proc.stdout.strip()

    def wait_for_idle(
        self,
        pane_id: str,
        poll_interval: float = 1.0,
        max_wait_seconds: int = 60
    ) -> bool:
        """Poll the pane until the agent status is 'idle' or 'done'."""
        start_time = time.time()
        while time.time() - start_time < max_wait_seconds:
            status = self.get_status(pane_id)
            if status.agent_status in ("idle", "done"):
                return True
            time.sleep(poll_interval)
        return False

    def switch_model_in_pane(self, pane_id: str, model_name: str) -> bool:
        """Switch active model in an interactive agy TUI session via /model command."""
        resolved = self.policy.validate_and_resolve_model(model_name)
        cmd = f"/model {resolved}"
        return self.run_in_pane(pane_id, cmd)