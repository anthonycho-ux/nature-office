#!/usr/bin/env python3
"""
Validation script for ensuring all coding agents follow the research requirements.

This script validates that:
1. New code includes proper research documentation
2. Research findings are stored in the research/ directory
3. All new features are backed by current web research
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def validate_research_directory():
    """Check that the research directory exists and contains proper documentation."""
    research_dir = Path("research")
    
    if not research_dir.exists():
        print("❌ ERROR: research/ directory not found")
        print("   All coding agents must store web research findings here")
        return False
    
    # Check for at least one recent research file
    research_files = list(research_dir.glob("*.md"))
    if not research_files:
        print("⚠️  WARNING: No research files found in research/ directory")
        print("   New research should be documented in research/ as markdown files")
    
    return True

def validate_contributing_file():
    """Check that CONTRIBUTING.md exists and contains research requirements."""
    contributing_path = Path("CONTRIBUTING.md")
    
    if not contributing_path.exists():
        print("❌ ERROR: CONTRIBUTING.md not found")
        print("   Research requirements must be documented in CONTRIBUTING.md")
        return False
    
    # Check for research requirements in the file
    content = contributing_path.read_text()
    research_keywords = [
        "web research",
        "Google AI",
        "research findings", 
        "research directory",
        "CONTRIBUTING.md"
    ]
    
    missing_keywords = []
    for keyword in research_keywords:
        if keyword.lower() not in content.lower():
            missing_keywords.append(keyword)
    
    if missing_keywords:
        print(f"⚠️  WARNING: CONTRIBUTING.md missing research keywords: {missing_keywords}")
        print("   Research requirements should be clearly documented")
    
    return True

def validate_code_changes():
    """Check that new code includes research documentation."""
    # This would be enhanced to check for research comments in new files
    # For now, we'll do a basic check for documentation
    
    python_files = list(Path("core").glob("*.py")) + list(Path("tooling").glob("*.py"))
    
    undocumented_files = []
    for py_file in python_files:
        content = py_file.read_text()
        # Check for research-related comments or documentation
        has_research_doc = any(
            keyword in content.lower() 
            for keyword in ["research", "web search", "google ai", "validation"]
        )
        
        if not has_research_doc and "def " in content:
            undocumented_files.append(str(py_file))
    
    if undocumented_files:
        print(f"⚠️  WARNING: The following Python files may lack research documentation:")
        for file in undocumented_files:
            print(f"   - {file}")
        print("   All new code should include research documentation")
    
    return True

def validate_research_files_format():
    """Check that research files follow the proper format."""
    research_dir = Path("research")
    
    if not research_dir.exists():
        return True
    
    research_files = list(research_dir.glob("*.md"))
    malformed_files = []
    
    for research_file in research_files:
        content = research_file.read_text()
        
        # Check for basic research format elements
        has_research_summary = "Research Summary:" in content
        has_sources = "Sources:" in content or "References:" in content
        has_impact = "Impact:" in content or "Implications:" in content
        
        if not (has_research_summary and has_sources and has_impact):
            malformed_files.append(str(research_file))
    
    if malformed_files:
        print(f"⚠️  WARNING: Research files may need better formatting:")
        for file in malformed_files:
            print(f"   - {file}")
        print("   Research files should include: Research Summary, Sources, Impact")
    
    return True

def main():
    """Main validation function."""
    print("🔍 Validating Agent Research Requirements")
    print("=" * 50)
    
    results = []
    
    # Run all validations
    results.append(("Research Directory", validate_research_directory()))
    results.append(("CONTRIBUTING.md", validate_contributing_file()))
    results.append(("Code Documentation", validate_code_changes()))
    results.append(("Research File Format", validate_research_files_format()))
    
    # Print summary
    print("\n📊 Validation Results:")
    print("-" * 30)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:25} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All research requirements validated successfully!")
        return 0
    else:
        print("⚠️  Some research requirements failed validation")
        print("\nNext steps:")
        print("1. Review CONTRIBUTING.md for incomplete research requirements")
        print("2. Create research/ directory if missing")
        print("3. Add research documentation to new code")
        print("4. Ensure research files follow proper format")
        return 1

if __name__ == "__main__":
    sys.exit(main())