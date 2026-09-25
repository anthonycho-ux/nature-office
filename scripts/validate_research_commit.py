#!/usr/bin/env python3
"""
Validate that commits include proper research documentation.

This script checks that commits involving new features include research references.
"""

import sys
import re
import subprocess
from pathlib import Path

def get_recent_commits(n: int = 5) -> list:
    """Get recent commit messages."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=format:%H|%s|%b"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                parts = line.split('|', 2)
                if len(parts) >= 2:
                    commits.append({
                        'hash': parts[0],
                        'subject': parts[1],
                        'body': parts[2] if len(parts) > 2 else ''
                    })
        return commits
    except subprocess.CalledProcessError:
        return []

def check_research_in_commit(commit: dict) -> tuple:
    """Check if a commit includes research references."""
    message = f"{commit['subject']} {commit['body']}".lower()
    
    # Keywords indicating research was done
    research_keywords = [
        'research',
        'web search',
        'google ai',
        'industry standard',
        'regulatory',
        'market analysis',
        'validation',
        'evidence-based',
        'finding',
        'discovered',
        'source:',
        'reference:'
    ]
    
    found_keywords = [kw for kw in research_keywords if kw in message]
    
    # Check if it's a feature commit (not docs, fix, chore, etc.)
    is_feature = any(prefix in commit['subject'].lower() for prefix in [
        'feat:', 'feature:', 'add:', 'implement:', 'create:', 'new:'
    ])
    
    # Feature commits must have research
    if is_feature and not found_keywords:
        return False, f"Feature commit '{commit['subject']}' missing research references"
    
    # All commits should have some research context for new functionality
    if is_feature and found_keywords:
        return True, f"Research keywords found: {found_keywords}"
    
    return True, "Not a feature commit or research present"

def main():
    """Main validation function."""
    print("🔍 Validating Research in Recent Commits")
    print("=" * 50)
    
    commits = get_recent_commits(10)
    
    if not commits:
        print("No commits found to validate")
        return 0
    
    all_valid = True
    
    for commit in commits:
        is_valid, message = check_research_in_commit(commit)
        status = "✅" if is_valid else "❌"
        print(f"{status} {commit['hash'][:8]}: {commit['subject']}")
        if not is_valid:
            print(f"   {message}")
            all_valid = False
        elif "Research keywords found" in message:
            print(f"   {message}")
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All feature commits include research references!")
        return 0
    else:
        print("⚠️  Some feature commits are missing research documentation")
        print("\nRequired: Feature commits must include research keywords such as:")
        print("  - 'research:' or 'web search:'")
        print("  - 'google ai' or 'industry standard'")
        print("  - 'regulatory' or 'market analysis'")
        print("  - 'validation' or 'source:'")
        return 1

if __name__ == "__main__":
    sys.exit(main())