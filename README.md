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

**IMPORTANT:** All coding agents working on this project **must** follow the web research requirements documented in [`CONTRIBUTING.md`](CONTRIBUTING.md). Research must be conducted using Google AI models and all findings documented in the `research/` directory.

## Architecture

```
nature-office/
├── core/
│   ├── __init__.py          # Package exports
│   ├── agy_bridge.py       # VehicleAssessmentService + OfficeReadyCertification
│   └── policy.py           # Certification criteria & model configuration
├── tooling/
│   └── scripts/            # Command-line tools
├── docs/                   # Documentation & guides
│   ├── architecture.md     # System architecture
│   └── research/          # Completed research documentation
├── scripts/                # Research and validation tools
│   ├── validate_research_requirements.py
│   ├── validate_research_commit.py
│   ├── create_research_summary.py
│   └── research_tools.py
├── research/               # Active research findings (NEW!)
│   ├── index.md
│   └── research.log
├── .github/workflows/     # GitHub Actions for research validation
│   └── agent-research-validation.yml
├── tests/                 # Test suite
└── CONTRIBUTING.md        # Research requirements for agents
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Assess a vehicle from photos and specs
```bash
python tooling/scripts/agy_cli.py assess \
    --vehicle-id VT001 \
    --photos photo1.jpg photo2.jpg \
    --specs specs.json
```

### 3. List certified vehicles
```bash
python tooling/scripts/agy_cli.py list --tier Executive
```

### 4. Research Integration (MANDATORY)
Before implementing any feature, conduct web research:

```bash
# Research tools automatically manage the workflow
cat > scripts/research_tools.py
# Follow guidelines in CONTRIBUTING.md
```

## Research Requirements

**Critical:** All coding agents must:

1. **Use Google AI models** for web research before implementing features
2. **Document findings** in the `research/` directory with proper formatting
3. **Update CONTRIBUTING.md** with new research requirements
4. **Validate commits** through GitHub Actions CI
5. **Reference sources** in code comments and documentation

Example research workflow:
```bash
# Use research tools
python scripts/research_tools.py

# Validate requirements
python scripts/validate_research_requirements.py

# Check commit compliance
python scripts/validate_research_commit.py
```

## Alberta Market Focus

### Target Segments
- **Calgary AI Companies** - High-tech sector requiring mobile offices
- **Edmonton Government Services** - Field-based administrative work
- **Field Service Teams** - Remote technical support and maintenance

### Certification Tiers
| Tier | Score Range | Multiplier | Daily Rate Range |
|------|-------------|------------|------------------|
| **Executive** | 90–100 | 2.0× | $600–$800 |
| **Professional**| 75–89 | 1.6× | $400–$550 |
| **Office** | 60–74 | 1.3× | $250–$350 |
| **Basic** | <60 | 1.0× | Not certified |

## Technical Features

### AI-Powered Assessment
- **5-Pillar Quality System**: Power, Connectivity, Workspace, Climate, Rest
- **Multi-Model Integration**: Claude, GPT, Gemini for comprehensive evaluation
- **Herdr Integration**: Real-time AI agent communication
- **Visual Analysis**: Photo-based vehicle feature detection

### 5-Pillar Certification

| Pillar | Weight | Alberta Standards | Key Requirements |
|--------|--------|-------------------|------------------|
| **Power** | 20% | Alberta energy codes | Solar arrays, battery systems, shore power |
| **Connectivity** | 20% | Canadian telecom standards | Starlink/5G, external antennas, redundancy |
| **Workspace** | 25% | Workplace safety codes | Ergonomic desks, client seating, cable management |
| **Climate** | 20% | Alberta climate requirements | Heating/AC, insulation, temperature control |
| **Rest** | 15% | Labor standards | Privacy, convertible seating, overnight capability |

## Requirements

- **Python 3.10+**
- **Herdr CLI** on PATH
- **Agy CLI** on PATH (for AI assessments)
- **GitHub Account** (for contribution workflow)

## Research Validation

This project enforces **evidence-based development** through:

1. **GitHub Actions CI** - Automated research validation
2. **Research Documentation** - All findings stored in `research/`
3. **Code Review** - Research references required in all new features
4. **Compliance Reporting** - Monthly research summaries

To begin, run the research tools:

```bash
# Initialize research workflow
python -c "from scripts.research_tools import example_research_workflow; example_research_workflow()"

# Validate research requirements
python scripts/validate_research_requirements.py
```

**Remember:** Every feature implementation must be preceded by comprehensive web research using Google's AI models. This ensures our solutions remain current, competitive, and compliant with Alberta's evolving requirements.

## License

MIT

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