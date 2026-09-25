"""
Policy and certification criteria for nature-office office-ready vehicle assessment.

This module defines the 5-pillar quality assessment system that determines whether
a vehicle qualifies as "office-ready" for mobile professional use.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set


class ExecutionMode(str, Enum):
    INTERACTIVE = "interactive"
    HEADLESS = "headless"
    BACKGROUND = "background"


@dataclass(frozen=True)
class OfficeReadyPolicy:
    """Policy rules for office-ready vehicle certification."""

    # 5-pillar assessment criteria for office-ready vehicles
    power_score: int = 20
    connectivity_score: int = 20
    workspace_score: int = 25
    climate_score: int = 20
    rest_score: int = 15

    # Minimum passing score for each pillar (4 = 80% of max)
    min_pillar_score: int = 4

    # Minimum total score for certification
    min_total_score: int = 60

    # Model configurations for AI-powered assessment
    default_model: str = "gemini-3.8-flash-high"
    timeout_seconds: int = 120
    max_read_lines: int = 200

    # Models officially supported for vehicle assessment
    allowed_models: Set[str] = field(default_factory=lambda: {
        "gemini-3.8-flash-high",
        "gemini-3.8-flash-medium",
        "gemini-3.8-flash-low",
        "gemini-3.7-flash-high",
        "gemini-3.7-flash-medium",
        "gemini-3.7-flash-low",
        "claude-sonnet-4-6",
        "claude-opus-4-6-thinking",
        "gpt-oss-120b-medium",
    })

    # Common aliases for model selection
    model_aliases: dict = field(default_factory=lambda: {
        "flash-high": "gemini-3.8-flash-high",
        "flash-med": "gemini-3.8-flash-medium",
        "flash-medium": "gemini-3.8-flash-medium",
        "flash-low": "gemini-3.8-flash-low",
        "claude": "claude-sonnet-4-6",
    })

    # Certification tier definitions
    tier_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "Executive": 2.0,
        "Professional": 1.6,
        "Office": 1.3,
        "Basic": 1.0,
    })

    # Pillar descriptions for documentation
    pillar_descriptions: Dict[str, str] = field(default_factory=lambda: {
        "power": "Power system capability for full workday operation",
        "connectivity": "Internet connectivity for reliable video calls",
        "workspace": "Dedicated workspace for 2-3 people",
        "climate": "Climate control for extreme temperatures",
        "rest": "Sleeping/rest area for overnight stays",
    })

    def validate_and_resolve_model(self, model_name: Optional[str]) -> str:
        """Resolve model alias and validate against allowed models list."""
        if not model_name:
            return self.default_model

        resolved = self.model_aliases.get(model_name.lower().strip(), model_name.strip())
        if resolved not in self.allowed_models:
            # Allow fallback if caller uses a newly released model string
            return resolved
        return resolved

    def sanitize_input(self, text: str) -> str:
        """Basic sanitization for input transmission."""
        if not text:
            return ""
        return text.replace("\x00", "").replace("\r\n", "\n")

    def get_tier_info(self, tier: str) -> Dict[str, float]:
        """Get pricing and score information for a certification tier."""
        return {
            "score_range": self._get_tier_score_range(tier),
            "multiplier": self.tier_multipliers.get(tier, 1.0),
        }

    def _get_tier_score_range(self, tier: str) -> str:
        """Get the score range for a certification tier."""
        if tier == "Executive":
            return "90–100"
        elif tier == "Professional":
            return "75–89"
        elif tier == "Office":
            return "60–74"
        else:
            return "<60"

    def is_certified(self, total_score: int, pillar_scores: Dict[str, int]) -> bool:
        """Check if a vehicle meets all certification requirements."""
        return (
            total_score >= self.min_total_score
            and all(score >= self.min_pillar_score for score in pillar_scores.values())
        )

    def get_tier_for_score(self, total_score: int) -> str:
        """Determine certification tier based on total score."""
        if total_score >= 90:
            return "Executive"
        elif total_score >= 75:
            return "Professional"
        elif total_score >= 60:
            return "Office"
        else:
            return "Basic"

    def calculate_daily_rate(self, base_rate: float, tier: str) -> float:
        """Calculate daily rental rate based on certification tier."""
        return base_rate * self.tier_multipliers.get(tier, 1.0)