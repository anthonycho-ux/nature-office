# Contributing to nature-office

## Agent Research Guidelines

When coding agents read this repository, they **must** conduct web research to supplement the information in the codebase. This ensures we have the latest information and maintains the competitive advantage of our solutions.

### Required Research Actions

1. **Google AI Model Web Research**
   - Before implementing any feature, use Google's Gemini or other Google AI models to search for:
     - Latest industry trends in mobile office solutions
     - Current regulations or certifications for mobile offices in Alberta
     - Recent technological advances in vehicle-based offices
     - New AI integration patterns for vehicle assessment

2. **Information Sources to Check**
   - Google Search: "mobile office vehicle certification 2026"
   - Industry blogs and whitepapers
   - Government regulations (Alberta Transportation/Air Quality)
   - Academic papers on vehicle-based workspaces
   - Latest AI model capabilities for visual assessment

3. **Research Integration**
   - Update documentation with findings
   - Modify assessment criteria if standards have changed
   - Add new features based on technological advances
   - Reference sources in code comments and documentation

### Research Workflow

```
Web Research → Analysis → Update Documentation → Implementation → Testing
```

### Required Documentation Updates

Every major feature implementation must include:
1. **Research Summary**: What was discovered and why it's relevant
2. **Source References**: Links to web research findings
3. **Impact Assessment**: How this affects the 5-pillar certification system
4. **Update Date**: Timestamp of the research

### Example Research Update Format

```markdown
## Research Updates: [Date]

### Topic: [Feature/Area]

**Discoveries:**
- [Latest industry trend or regulation]
- [New technology or standard]
- [Competitor innovation]

**Impact:**
- [How this affects our implementation]
- [Required changes to certification criteria]

**Sources:**
- [Google search results]
- [Industry paper/website]
- [Regulatory document link]
```

### Automated Research Trigger

This repository should be configured with a system that prompts new coding agents to:

1. Start by running web research using Google's AI models
2. Document all findings in the `research/` directory
3. Update the `requirements.txt` if new dependencies are discovered
4. Update the `CONTRIBUTING.md` with new research findings

### Research Priority

Always prioritize:
1. **Regulatory changes** (Alberta transportation/air quality standards)
2. **Technology advances** (battery systems, connectivity, workspace tech)
3. **Market trends** (demand for mobile AI offices)
4. **Security and privacy** (data protection in mobile offices)

### Quality Standards for Research

- **Currency**: All information must be from 2024-2026
- **Authority**: Prefer official government documents, peer-reviewed papers, industry experts
- **Completeness**: Research must cover technical, regulatory, and market aspects
- **Verification**: Cross-reference findings from multiple sources

### Research Team Configuration

To ensure consistent research across coding agents:

1. **Research prompts**: Pre-written Google AI prompts for common research tasks
2. **Source templates**: Standardized format for citing research findings
3. **Research milestones**: Checkpoints where research must be completed
4. **Quality review**: Human-in-the-loop validation of important research findings

### Research Documentation

All research findings should be stored in:

- `research/` - New research findings and discoveries
- `docs/research/` - Completed research with analysis and recommendations
- `README.md` - Updated with latest research insights
- `CONTRIBUTING.md` - Updated with new research requirements

### Example Research Task

**Task**: Implement Alberta-specific mobile office certification updates

**Required Research Actions**:
1. Search "Alberta mobile office regulations 2026"
2. Review "mobile office vehicle standards" on official Alberta government sites
3. Analyze "Alberta AI office requirements" from tech industry reports
4. Check "Canada transportation mobile workspace standards" for cross-border implications
5. Research "Starlink Alberta mobile office connectivity requirements"

**Deliverables**:
1. Updated `core/policy.py` with new Alberta-specific criteria
2. Research documentation in `research/alberta-2026.md`
3. Updated documentation in `docs/compliance-alberta.md`
4. Updated test cases in `tests/alberta-requirements.md`

### Research Success Metrics

An agent has successfully completed research when:

1. **Knowledge Integration**: The codebase now includes at least 3 new research findings
2. **Documentation Updated**: All findings are properly documented and referenced
3. **Tests Added**: New research-based test cases are included
4. **Dependencies Updated**: `requirements.txt` includes relevant research tools
5. **Quality Reviewed**: Research has been validated against current standards

### Research Safety and Ethics

All research must adhere to:
- **Copyright compliance** when citing industry sources
- **Data privacy** when researching customer information
- **AI model usage policies** for Google/AI research
- **Industry standards** for competitive intelligence

### Research Timeline

- **Weekly**: Team shares new research discoveries
- **Monthly**: Update documentation with latest findings
- **Quarterly**: Review and validate all research against current standards
- **Annually**: Complete research audit and plan next year's priorities

By following these research guidelines, nature-office maintains its position as a cutting-edge solution in the mobile office market, constantly incorporating the latest technological advances and regulatory requirements.