#!/usr/bin/env python3
"""
Simple setup verification script for Paper2Data monorepo.

Validates that all required files and directories exist and basic structure is correct.
Does not require external dependencies.
"""

import os
import sys
from pathlib import Path


def check_file_exists(path, description):
    """Check if a file exists and print result."""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} (MISSING)")
        return False


def check_directory_exists(path, description):
    """Check if a directory exists and print result."""
    if Path(path).is_dir():
        print(f"✅ {description}: {path}/")
        return True
    else:
        print(f"❌ {description}: {path}/ (MISSING)")
        return False


def validate_file_content(path, required_strings, description):
    """Validate that a file contains required strings."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        for required in required_strings:
            if required not in content:
                missing.append(required)
        
        if not missing:
            print(f"✅ {description}: Content validation passed")
            return True
        else:
            print(f"❌ {description}: Missing content - {missing}")
            return False
    except Exception as e:
        print(f"❌ {description}: Error reading file - {e}")
        return False


def main():
    """Main validation function."""
    print("🔍 Paper2Data Setup Verification")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    all_checks_passed = True
    
    # Check main directories
    print("\n📁 Directory Structure:")
    directories = [
        ("packages", "Packages directory"),
        ("packages/parser", "Python parser package"),
        ("packages/cli", "Node.js CLI package"),
        ("Docs", "Documentation"),
        ("config", "Configuration"),
        ("tests", "Test directory"),
        ("examples", "Examples directory")
    ]
    
    for dir_path, description in directories:
        if not check_directory_exists(dir_path, description):
            all_checks_passed = False
    
    # Check essential files
    print("\n📄 Essential Files:")
    files = [
        ("README.md", "Main README"),
        (".gitignore", "Git ignore file"),
        ("packages/parser/pyproject.toml", "Python package config"),
        ("packages/cli/package.json", "Node.js package config"),
        ("packages/cli/src/index.js", "CLI entry point"),
        ("Docs/Implementation.md", "Implementation plan"),
        ("Docs/project_structure.md", "Project structure doc"),
        ("Docs/UI_UX_doc.md", "UI/UX documentation"),
        ("config/github-actions.yml", "CI/CD configuration"),
        ("config/linting/flake8.ini", "Python linting config"),
        ("config/linting/eslint.json", "JavaScript linting config")
    ]
    
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check Python package structure
    print("\n🐍 Python Package Structure:")
    python_files = [
        ("packages/parser/src/paper2data/ingest.py", "Ingestion module"),
        ("packages/parser/src/paper2data/extractor.py", "Extraction module"),
        ("packages/parser/src/paper2data/utils.py", "Utilities module"),
        ("packages/parser/src/paper2data/__init__.py", "Python package init"),
        ("packages/parser/src/paper2data/main.py", "Main CLI module"),
        ("packages/parser/src/paper2data/__main__.py", "Package entry point"),
        ("packages/parser/tests/test_parser.py", "Parser tests")
    ]
    
    for file_path, description in python_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check Node.js CLI structure
    print("\n🔧 Node.js CLI Structure:")
    cli_files = [
        ("packages/cli/src/commands/init.js", "Init command"),
        ("packages/cli/src/commands/convert.js", "Convert command"),
        ("packages/cli/tests/test_cli.js", "CLI tests")
    ]
    
    for file_path, description in cli_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Validate key file contents
    print("\n📋 Content Validation:")
    
    # Check package.json
    if Path("packages/cli/package.json").exists():
        validate_file_content(
            "packages/cli/package.json",
            ["paper2data-cli", "commander", "chalk"],
            "CLI package.json"
        )
    
    # Check pyproject.toml
    if Path("packages/parser/pyproject.toml").exists():
        validate_file_content(
            "packages/parser/pyproject.toml",
            ["paper2data-parser", "PyMuPDF", "pdfplumber"],
            "Parser pyproject.toml"
        )
    
    # Check CLI entry point
    if Path("packages/cli/src/index.js").exists():
        validate_file_content(
            "packages/cli/src/index.js",
            ["#!/usr/bin/env node", "commander", "paper2data"],
            "CLI entry point"
        )
    
    # Final summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 SUCCESS: Paper2Data monorepo setup is complete!")
        print("\n✅ Ready for Stage 1 implementation:")
        print("   • Project structure is correctly organized")
        print("   • All required files and directories exist")
        print("   • Package configurations are in place")
        print("   • Documentation structure is ready")
        print("   • CI/CD configuration is available")
        print("\n🚀 Next steps:")
        print("   1. Install Node.js dependencies: cd packages/cli && npm install")
        print("   2. Setup Python environment: cd packages/parser && python -m venv venv")
        print("   3. Install Python dependencies: pip install -e '.[dev]'")
        print("   4. Start implementing Stage 1 tasks from Implementation.md")
        return 0
    else:
        print("❌ FAILED: Some files or directories are missing")
        print("   Please check the errors above and ensure all files are created")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 