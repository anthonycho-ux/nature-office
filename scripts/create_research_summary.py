#!/usr/bin/env python3
"""
Create a research validation summary for the project.

This script generates a summary report of all research activities
and their integration into the codebase.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_research_summary():
    """Generate a comprehensive research summary."""
    summary = {
        "project": "nature-office",
        "timestamp": datetime.now().isoformat(),
        "research_directories": [],
        "research_files": [],
        "code_research_integration": [],
        "recommendations": []
    }
    
    # Check research directory
    research_dir = Path("research")
    if research_dir.exists():
        summary["research_directories"].append(str(research_dir))
        for file in research_dir.glob("*.md"):
            summary["research_files"].append({
                "file": str(file),
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    # Check docs/research directory
    docs_research = Path("docs/research")
    if docs_research.exists():
        summary["research_directories"].append(str(docs_research))
        for file in docs_research.glob("*.md"):
            summary["research_files"].append({
                "file": str(file),
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    # Check for research references in code
    code_dirs = ["core", "tooling", "docs"]
    for code_dir in code_dirs:
        code_path = Path(code_dir)
        if code_path.exists():
            for py_file in code_path.glob("*.py"):
                content = py_file.read_text()
                research_refs = []
                
                # Look for research keywords
                research_keywords = [
                    "research", "web search", "google ai", "industry standard",
                    "regulatory", "market analysis", "validation", "evidence",
                    "source:", "reference:", "finding:", "discovered"
                ]
                
                for keyword in research_keywords:
                    if keyword in content.lower():
                        research_refs.append(keyword)
                
                if research_refs:
                    summary["code_research_integration"].append({
                        "file": str(py_file),
                        "research_keywords": research_refs
                    })
    
    # Generate recommendations
    if not summary["research_files"]:
        summary["recommendations"].append("No research files found - agents must conduct web research and document findings")
    
    if len(summary["code_research_integration"]) < 2:
        summary["recommendations"].append("Limited research integration in code - new features should reference research")
    
    if not Path("CONTRIBUTING.md").exists():
        summary["recommendations"].append("CONTRIBUTING.md missing - research requirements must be documented")
    
    return summary

def print_summary(summary: dict):
    """Print a formatted research summary."""
    print("📊 Research Validation Summary")
    print("=" * 50)
    print(f"Project: {summary['project']}")
    print(f"Generated: {summary['timestamp']}")
    print()
    
    print(f"📁 Research Directories: {len(summary['research_directories'])}")
    for d in summary['research_directories']:
        print(f"   - {d}")
    print()
    
    print(f"📄 Research Files: {len(summary['research_files'])}")
    for f in summary['research_files']:
        print(f"   - {f['file']} ({f['size']} bytes, modified: {f['modified'][:10]})")
    print()
    
    print(f"🔗 Code Research Integration: {len(summary['code_research_integration'])} files")
    for c in summary['code_research_integration']:
        print(f"   - {c['file']}: {', '.join(c['research_keywords'])}")
    print()
    
    if summary['recommendations']:
        print("⚠️  Recommendations:")
        for r in summary['recommendations']:
            print(f"   - {r}")
    else:
        print("✅ No recommendations - research practices look good!")

def main():
    """Main function."""
    summary = generate_research_summary()
    print_summary(summary)
    
    # Save to file
    output_file = Path("research") / f"summary_{datetime.now().strftime('%Y%m%d')}.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(summary, indent=2))
    print(f"\n💾 Summary saved to: {output_file}")
    
    # Return exit code based on recommendations
    return 1 if summary['recommendations'] else 0

if __name__ == "__main__":
    exit(main())