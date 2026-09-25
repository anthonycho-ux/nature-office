# nature-office

**Alberta's premium mobile office solution for AI professionals.**

A marketplace connecting idle RV/cargo van owners with AI consulting firms
and government agencies that need certified mobile office vehicles.

## Overview

`nature-office` provides AI-powered office-ready vehicle certification
and a two-sided marketplace for mobile office rentals in Alberta.

- **Supply side:** RV/cargo van owners with idle vehicles
- **Demand side:** AI consulting firms, government agencies, field service teams
- **Differentiator:** 5-pillar quality certification (power, connectivity,
  workspace, climate, rest) with Executive / Professional / Office / Basic tiers

## Architecture

```
nature-office/
├── core/
│   ├── agy_bridge.py       # VehicleAssessmentService + OfficeReadyCertification
│   └── policy.py           # Certification criteria & model configuration
├── tooling/scripts/
│   └── agy_cli.py          # CLI for assessment, listing, and booking
├── docs/
│   └── certification.md    # Full 5-pillar scoring rubric
└── tests/
    └── test_assessment.py  # Unit tests for VehicleAssessmentService
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Assess a vehicle from photos and specs
python tooling/scripts/agy_cli.py assess \
    --vehicle-id VT001 \
    --photos photo1.jpg,photo2.jpg \
    --specs specs.json

# List certified vehicles
python tooling/scripts/agy_cli.py list --tier Executive
```

## Certification Tiers

| Tier        | Score Range | Multiplier | Example Daily Rate |
|-------------|-------------|------------|--------------------|
| Executive   | 90–100      | 2.0×       | $600–$800          |
| Professional| 75–89       | 1.6×       | $400–$550          |
| Office      | 60–74       | 1.3×       | $250–$350          |
| Basic       | <60         | 1.0×       | Not listed         |

## Requirements

- Python 3.10+
- `herdr` CLI on PATH
- `agy` CLI on PATH (optional, for AI-powered assessment)

## License

MIT