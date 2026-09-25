"""CLI tool for nature-office vehicle assessment and management.

This module provides command-line interfaces for:
1. Assessing vehicles for office-readiness
2. Listing certified vehicles
3. Managing vehicle assessments

The tool uses the agy_bridge module to perform AI-powered vehicle assessments
using Claude, GPT, and Gemini models for comprehensive quality analysis.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

from core.agy_bridge import AgyBridge
from core.policy import OfficeReadyPolicy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NatureOfficeCLI:
    """Command-line interface for nature-office vehicle assessment and management."""

    def __init__(self):
        self.policy = OfficeReadyPolicy()
        self.agy_bridge = AgyBridge(self.policy)

    def assess_vehicle(self, vehicle_id: str, photos: List[str], specs: str) -> None:
        """Assess a vehicle for office-readiness."""
        try:
            # Parse specifications
            spec_dict = json.loads(specs) if specs else {}

            logger.info(f"Assessing vehicle {vehicle_id}...")

            # Perform vehicle assessment
            result = self.agy_bridge.assess_vehicle(vehicle_id, photos, spec_dict)

            # Display assessment results
            self._display_assessment_result(result)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in specifications: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error assessing vehicle: {e}")
            sys.exit(1)

    def list_certified_vehicles(self, tier: Optional[str] = None, min_score: int = 0) -> None:
        """List certified vehicles."""
        logger.info("Listing certified vehicles...")

        # In a real implementation, this would query a database
        # For now, we'll show a sample output
        vehicles = self._get_certified_vehicles(tier, min_score)

        if not vehicles:
            print("No certified vehicles found.")
            return

        print("Certified Vehicles:")
        print("=" * 80)
        for vehicle in vehicles:
            print(f"Vehicle ID: {vehicle['vehicle_id']}")
            print(f"  Tier: {vehicle['tier']}")
            print(f"  Total Score: {vehicle['total_score']}")
            print(f"  Daily Rate: ${vehicle['daily_rate']:.2f}")
            print(f"  Pillar Scores: {vehicle['pillar_scores']}")
            print()

    def _display_assessment_result(self, result: Dict[str, Any]) -> None:
        """Display vehicle assessment results in a formatted way."""
        print("=" * 80)
        print("VEHICLE ASSESSMENT RESULTS")
        print("=" * 80)
        print(f"Vehicle ID: {result['vehicle_id']}")
        print(f"Assessment ID: {result['assessment_id']}")
        print("\n📊 SCORE SUMMARY")
        print("-" * 40)
        print(f"Total Score: {result['total_score']}/100")
        print(f"Certification Tier: {result['tier']}")
        print(f"Commission Multiplier: {result['multiplier']:.1f}×")

        print("\n📋 PILLAR SCORES")
        print("-" * 40)
        for pillar, score in result['pillar_scores'].items():
            max_score = {
                'power': 20,
                'connectivity': 20,
                'workspace': 25,
                'climate': 20,
                'rest': 15,
            }.get(pillar, 0)
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            print(f"{pillar.title()}: {score}/{max_score} ({percentage:.1f}%)")

        print("\n💡 RECOMMENDATIONS")
        if result['recommendations']:
            for i, recommendation in enumerate(result['recommendations'], 1):
                print(f"  {i}. {recommendation}")
        else:
            print("  No improvements recommended - vehicle is well-suited for office use!")

        print("\n💰 FINANCIAL IMPLICATIONS")
        print("-" * 40)
        # This would need to be calculated based on actual rental rates
        print(f"Base Rate: $500/day (estimated)")
        print(f"Commission Rate: {result['multiplier'] * 100:.0f}%")
        print(f"Estimated Daily Revenue: ${500 * result['multiplier']:.2f}")

        print("\n" + "=" * 80)

    def _get_certified_vehicles(self, tier: Optional[str], min_score: int) -> List[Dict[str, Any]]:
        """Get list of certified vehicles (mock implementation)."""
        mock_vehicles = [
            {
                "vehicle_id": "VT001",
                "tier": "Executive",
                "total_score": 95,
                "daily_rate": 800,
                "pillar_scores": {"power": 20, "connectivity": 20, "workspace": 25, "climate": 20, "rest": 10},
            },
            {
                "vehicle_id": "VT002",
                "tier": "Professional",
                "total_score": 82,
                "daily_rate": 550,
                "pillar_scores": {"power": 18, "connectivity": 18, "workspace": 23, "climate": 18, "rest": 5},
            },
            {
                "vehicle_id": "VT003",
                "tier": "Office",
                "total_score": 68,
                "daily_rate": 320,
                "pillar_scores": {"power": 12, "connectivity": 12, "workspace": 18, "climate": 12, "rest": 14},
            },
        ]

        filtered_vehicles = [
            v for v in mock_vehicles
            if (not tier or v['tier'] == tier) and v['total_score'] >= min_score
        ]

        return filtered_vehicles

    def create_sample_assessment(self, vehicle_id: str) -> Dict[str, Any]:
        """Create a sample assessment for demonstration purposes."""
        return {
            "vehicle_id": vehicle_id,
            "assessment_id": f"sample_{vehicle_id}",
            "timestamp": time.time(),
            "visual_assessment": {
                "vehicle_id": vehicle_id,
                "photo_count": 4,
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
            },
            "technical_validation": {
                "vehicle_id": vehicle_id,
                "pillar_scores": {
                    "power": 18,
                    "connectivity": 18,
                    "workspace": 22,
                    "climate": 18,
                    "rest": 10,
                },
                "total_score": 86,
                "tier": "Professional",
                "validated_at": time.time(),
            },
            "assessment": {
                "vehicle_id": vehicle_id,
                "total_score": 86,
                "tier": "Professional",
                "pillar_scores": {
                    "power": 18,
                    "connectivity": 18,
                    "workspace": 22,
                    "climate": 18,
                    "rest": 10,
                },
                "multiplier": 1.6,
                "recommendations": [
                    "Consider upgrading power system for longer runtime",
                    "Add external antenna for better connectivity",
                ],
                "assessment_completed_at": time.time(),
            },
            "tier": "Professional",
            "multiplier": 1.6,
            "pillar_scores": {
                "power": 18,
                "connectivity": 18,
                "workspace": 22,
                "climate": 18,
                "rest": 10,
            },
            "recommendations": [
                "Consider upgrading power system for longer runtime",
                "Add external antenna for better connectivity",
            ],
        }


def main():
    """Main entry point for the CLI."""
    cli = NatureOfficeCLI()
    parser = argparse.ArgumentParser(
        description="nature-office: AI-powered vehicle assessment for office-readiness"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Assess vehicle command
    assess_parser = subparsers.add_parser("assess", help="Assess a vehicle")
    assess_parser.add_argument("--vehicle-id", required=True, help="Vehicle ID")
    assess_parser.add_argument("--photos", nargs="+", help="Photo files")
    assess_parser.add_argument("--specs", help="JSON specifications")

    # List vehicles command
    list_parser = subparsers.add_parser("list", help="List certified vehicles")
    list_parser.add_argument("--tier", choices=["Executive", "Professional", "Office", "Basic"], help="Certification tier")
    list_parser.add_argument("--min-score", type=int, default=0, help="Minimum total score")

    # Sample assessment command
    subparsers.add_parser("sample", help="Generate a sample assessment")

    args = parser.parse_args()

    if args.command == "assess":
        if args.photos:
            # Ensure photos exist
            for photo in args.photos:
                if not os.path.exists(photo):
                    logger.error(f"Photo file not found: {photo}")
                    sys.exit(1)

            cli.assess_vehicle(args.vehicle_id, args.photos, args.specs or "{}")
        else:
            logger.error("At least one photo file must be provided")
            sys.exit(1)

    elif args.command == "list":
        cli.list_certified_vehicles(args.tier, args.min_score)

    elif args.command == "sample":
        sample = cli.create_sample_assessment(args.vehicle_id)
        print("=" * 80)
        print("SAMPLE ASSESSMENT RESULT")
        print("=" * 80)

        # Display assessment results
        cli._display_assessment_result(sample)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    import time
    main()