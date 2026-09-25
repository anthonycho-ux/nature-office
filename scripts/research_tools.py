"""
Research tools for coding agents in the nature-office project.

This module provides functions to help coding agents conduct web research
as required by the project's contributing guidelines.
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

class ResearchTools:
    """Tools for conducting web research as required by nature-office guidelines."""
    
    def __init__(self, research_dir: str = "research"):
        self.research_dir = Path(research_dir)
        self.research_dir.mkdir(exist_ok=True)
    
    def create_research_summary(self, topic: str, findings: List[Dict], 
                               sources: List[str], impact: str) -> str:
        """
        Create a research summary markdown file.
        
        Args:
            topic: The research topic
            findings: List of key findings with details
            sources: List of source URLs or references
            impact: How this research impacts the project
            
        Returns:
            Path to the created research file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"research/{timestamp}_{topic.lower().replace(' ', '-')}.md"
        
        content = f"""# Research: {topic}

## Date
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Research Summary
{self._format_findings(findings)}

## Sources
{self._format_sources(sources)}

## Impact on Project
{impact}

## Verification Status
- [ ] Validated by human reviewer
- [ ] Cross-referenced with other sources
- [ ] Integrated into implementation
- [ ] Documentation updated

## Next Steps
- [ ] Update core/policy.py if new standards discovered
- [ ] Add tests for new requirements
- [ ] Update documentation
- [ ] Share findings with team
"""
        
        filepath = Path(filename)
        filepath.write_text(content)
        
        # Update research index
        self._update_research_index(topic, filename, timestamp)
        
        return str(filepath)
    
    def _format_findings(self, findings: List[Dict]) -> str:
        """Format research findings for the research summary."""
        if not findings:
            return "No key findings identified."
        
        formatted = "Key discoveries:\n"
        for i, finding in enumerate(findings, 1):
            title = finding.get("title", f"Finding {i}")
            detail = finding.get("detail", "")
            formatted += f"\n{i}. **{title}**
   {detail}\n"
        
        return formatted
    
    def _format_sources(self, sources: List[str]) -> str:
        """Format sources for the research summary."""
        if not sources:
            return "No sources recorded."
        
        formatted = ""
        for i, source in enumerate(sources, 1):
            formatted += f"{i}. {source}\n"
        
        return formatted
    
    def _update_research_index(self, topic: str, filename: str, date: str):
        """Update the research index with new research."""
        index_file = self.research_dir / "index.md"
        
        if not index_file.exists():
            content = f"""# Research Index

## Recent Research
| Date | Topic | File |
|------|-------|------|
| {date} | {topic} | {filename} |
"""
            index_file.write_text(content)
        else:
            # Read existing content and add new entry
            content = index_file.read_text()
            if "| Date | Topic | File |" not in content:
                # Insert new header and first row
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.strip() == "## Recent Research":
                        # Add table header
                        new_lines.append("| Date | Topic | File |")
                        new_lines.append("|------|-------|------|")
                        # Add new row
                        new_lines.append(f"| {date} | {topic} | {filename} |")
                        break
                
                index_file.write_text('\n'.join(new_lines))
            else:
                # Just add new row at the end of the table
                lines = content.split('\n')
                new_lines = []
                added = False
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.strip().startswith("| -----") and i < len(lines) - 1:
                        # Add new row before next section
                        new_lines.append(f"| {date} | {topic} | {filename} |")
                        added = True
                
                if not added:
                    # Append to end of file
                    new_lines.append(f"| {date} | {topic} | {filename} |")
                
                index_file.write_text('\n'.join(new_lines))
    
    def validate_implementation(self, research_topic: str, implementation_file: str) -> bool:
        """
        Validate that an implementation includes research findings.
        
        Args:
            research_topic: The topic that should be referenced
            implementation_file: Path to the implementation file
            
        Returns:
            True if implementation appears to include research, False otherwise
        """
        filepath = Path(implementation_file)
        
        if not filepath.exists():
            return False
        
        content = filepath.read_text()
        
        # Check for research-related keywords
        research_indicators = [
            "research",
            "web search",
            "google ai",
            "validation",
            "industry standard",
            "regulatory requirement",
            "market research"
        ]
        
        return any(indicator in content.lower() for indicator in research_indicators)
    
    def create_research_prompt(self, feature_name: str, technical_requirements: List[str]) -> str:
        """
        Create a research prompt for Google AI model.
        
        Args:
            feature_name: Name of the feature being researched
            technical_requirements: List of technical requirements to research
            
        Returns:
            Formatted research prompt
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""# Research Request: {feature_name}

## Date
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Research Purpose
Conduct web research to inform the development of: {feature_name}

## Technical Requirements to Research
{chr(10).join(f"- {req}" for req in technical_requirements)}

## Research Instructions
Please provide information on:

1. **Latest Industry Standards**
   - Current regulations for {feature_name}
   - Industry best practices
   - Certification requirements (if applicable)

2. **Technological Advances**
   - New technologies relevant to {feature_name}
   - Recent innovations or breakthroughs
   - Integration considerations

3. **Market Trends**
   - Current demand for {feature_name}
   - Competitive landscape
   - Customer requirements

4. **Regulatory Compliance**
   - Legal requirements for {feature_name}
   - Compliance standards
   - Verification processes

## Research Output Format
Please format your response as:

**Research Summary:**
[Brief summary of key findings]

**Key Discoveries:**
1. [Discovery 1]
2. [Discovery 2]
3. [Discovery 3]

**Impact Assessment:**
[This feature impacts the following aspects:]

**Sources:**
1. [Source 1 URL]
2. [Source 2 URL]

## Validation Required
Please verify this information with at least 2-3 different sources for accuracy.

This research is part of the nature-office project's commitment to evidence-based development.
"""
        
        return prompt
    
    def log_research_process(self, topic: str, action: str, details: str = ""):
        """
        Log research activities for tracking and accountability.
        
        Args:
            topic: Research topic being conducted
            action: Action being performed (e.g., "searching", "analyzing", "validating")
            details: Additional details about the action
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"[{timestamp}] Research: {topic} - {action} - {details}\n"
        
        log_file = self.research_dir / "research.log"
        log_file.write_text(log_entry, mode='a')


def example_research_workflow():
    """Example of how to use the research tools."""
    # Initialize research tools
    research = ResearchTools()
    
    # Example: Research for a new vehicle assessment feature
    feature_name = "Advanced Solar Integration"
    technical_requirements = [
        "Latest solar panel efficiency standards",
        "Alberta solar installation regulations",
        "Vehicle power management optimization",
        "Industry solar integration best practices"
    ]
    
    # Create research prompt
    prompt = research.create_research_prompt(feature_name, technical_requirements)
    print("Research prompt created:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    
    # Example: Log research activity
    research.log_research_process(
        topic=feature_name,
        action="conducting web search",
        details="Using Google AI model for solar integration research"
    )

if __name__ == "__main__":
    example_research_workflow()