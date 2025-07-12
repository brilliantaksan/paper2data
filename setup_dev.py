#!/usr/bin/env python3
"""
Paper2Data Development Environment Setup

Automated setup script for Paper2Data development environment.
Sets up both Python parser and Node.js CLI packages.
"""

import sys
import subprocess
import shutil
import os
from pathlib import Path
import platform

def print_status(message: str, status: str = "info"):
    """Print colored status messages."""
    colors = {
        "info": "\033[94m",     # Blue
        "success": "\033[92m",  # Green
        "warning": "\033[93m",  # Yellow
        "error": "\033[91m",    # Red
        "reset": "\033[0m"      # Reset
    }
    
    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    color = colors.get(status, colors["info"])
    symbol = symbols.get(status, "•")
    reset = colors["reset"]
    
    print(f"{color}{symbol} {message}{reset}")

def run_command(command: list, cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    try:
        print_status(f"Running: {' '.join(command)}", "info")
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print_status(f"Command failed: {e}", "error")
        if e.stderr:
            print(f"  Error: {e.stderr.strip()}")
        raise

def check_prerequisites():
    """Check if required tools are installed."""
    print_status("Checking prerequisites...", "info")
    
    # Check Python 3.10+
    try:
        result = run_command(["python3", "--version"], check=False)
        version_str = result.stdout.strip()
        if result.returncode == 0:
            # Extract version number
            version_parts = version_str.split()[1].split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            if major >= 3 and minor >= 10:
                print_status(f"Python version: {version_str}", "success")
            else:
                print_status(f"Python 3.10+ required, found: {version_str}", "error")
                return False
        else:
            print_status("Python 3 not found", "error")
            return False
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_status("Python 3 not found", "error")
        return False
    
    # Check Node.js 16+
    try:
        result = run_command(["node", "--version"], check=False)
        version_str = result.stdout.strip()
        if result.returncode == 0:
            # Extract version number
            version_parts = version_str[1:].split('.')  # Remove 'v' prefix
            major = int(version_parts[0])
            if major >= 16:
                print_status(f"Node.js version: {version_str}", "success")
            else:
                print_status(f"Node.js 16+ required, found: {version_str}", "error")
                return False
        else:
            print_status("Node.js not found", "error")
            return False
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_status("Node.js not found", "error")
        return False
    
    # Check npm
    try:
        result = run_command(["npm", "--version"], check=False)
        if result.returncode == 0:
            print_status(f"npm version: {result.stdout.strip()}", "success")
        else:
            print_status("npm not found", "error")
            return False
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_status("npm not found", "error")
        return False
    
    # Check git
    try:
        result = run_command(["git", "--version"], check=False)
        if result.returncode == 0:
            print_status(f"Git version: {result.stdout.strip()}", "success")
        else:
            print_status("Git not found (optional but recommended)", "warning")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print_status("Git not found (optional but recommended)", "warning")
    
    return True

def setup_python_environment():
    """Set up Python virtual environment and install dependencies."""
    print_status("Setting up Python environment...", "info")
    
    parser_dir = Path("packages/parser")
    venv_dir = parser_dir / "venv"
    
    # Create virtual environment
    if not venv_dir.exists():
        print_status("Creating Python virtual environment...", "info")
        run_command(["python3", "-m", "venv", "venv"], cwd=parser_dir)
    else:
        print_status("Virtual environment already exists", "success")
    
    # Determine activation script based on platform
    if platform.system() == "Windows":
        activate_script = venv_dir / "Scripts" / "activate"
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Install dependencies
    print_status("Installing Python dependencies...", "info")
    run_command([str(pip_exe), "install", "--upgrade", "pip"], cwd=parser_dir)
    run_command([str(pip_exe), "install", "-e", ".[dev]"], cwd=parser_dir)
    
    print_status("Python environment setup complete", "success")
    return python_exe, pip_exe, activate_script

def setup_nodejs_environment():
    """Set up Node.js environment and install dependencies."""
    print_status("Setting up Node.js environment...", "info")
    
    cli_dir = Path("packages/cli")
    
    # Install dependencies
    print_status("Installing Node.js dependencies...", "info")
    run_command(["npm", "install"], cwd=cli_dir)
    
    # Link CLI for global usage (optional)
    try:
        print_status("Linking CLI for global usage...", "info")
        run_command(["npm", "link"], cwd=cli_dir)
        print_status("CLI linked globally - you can now use 'paper2data' command", "success")
    except subprocess.CalledProcessError:
        print_status("Failed to link CLI globally (may require sudo)", "warning")
        print_status("You can still use: npm run start -- <arguments>", "info")
    
    print_status("Node.js environment setup complete", "success")

def run_tests():
    """Run tests to verify installation."""
    print_status("Running tests to verify installation...", "info")
    
    # Test Python package
    try:
        print_status("Testing Python parser package...", "info")
        parser_dir = Path("packages/parser")
        
        # Use virtual environment python
        if platform.system() == "Windows":
            python_exe = parser_dir / "venv" / "Scripts" / "python.exe"
        else:
            python_exe = parser_dir / "venv" / "bin" / "python"
        
        run_command([str(python_exe), "-m", "pytest", "-v"], cwd=parser_dir)
        print_status("Python tests passed", "success")
    except subprocess.CalledProcessError:
        print_status("Python tests failed", "error")
        return False
    
    # Test Node.js CLI
    try:
        print_status("Testing Node.js CLI package...", "info")
        cli_dir = Path("packages/cli")
        run_command(["npm", "test"], cwd=cli_dir)
        print_status("Node.js tests passed", "success")
    except subprocess.CalledProcessError:
        print_status("Node.js tests failed", "error")
        return False
    
    # Test integration
    try:
        print_status("Testing CLI-Python integration...", "info")
        run_command(["python3", "tests/integration_test.py"])
        print_status("Integration tests passed", "success")
    except subprocess.CalledProcessError:
        print_status("Integration tests failed", "error")
        return False
    
    return True

def create_sample_config():
    """Create sample configuration files."""
    print_status("Creating sample configuration...", "info")
    
    # Create sample paper2data.yml
    config_content = """# Paper2Data Configuration
output:
  format: json
  directory: ./paper2data_output
  preserve_structure: true

processing:
  extract_figures: true
  extract_tables: true
  extract_citations: true
  max_file_size_mb: 100

logging:
  level: INFO
  file: null
"""
    
    config_file = Path("paper2data.sample.yml")
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print_status(f"Sample config created: {config_file}", "success")

def print_usage_instructions():
    """Print usage instructions."""
    print_status("Setup completed successfully!", "success")
    print("\n" + "="*60)
    print("📚 USAGE INSTRUCTIONS")
    print("="*60)
    
    print("\n🐍 Python Package Usage:")
    if platform.system() == "Windows":
        print("  # Activate virtual environment")
        print("  cd packages/parser")
        print("  venv\\Scripts\\activate")
    else:
        print("  # Activate virtual environment")
        print("  cd packages/parser")
        print("  source venv/bin/activate")
    
    print("  # Use the parser directly")
    print("  python -m paper2data.parser convert sample.pdf")
    print("  python -m paper2data.parser validate https://arxiv.org/abs/2301.00001")
    
    print("\n🌐 CLI Usage:")
    print("  # If globally linked")
    print("  paper2data convert sample.pdf")
    print("  paper2data convert https://arxiv.org/abs/2301.00001 --output ./my_output")
    print("  paper2data convert validate sample.pdf")
    
    print("  # Or using npm")
    print("  cd packages/cli")
    print("  npm start convert sample.pdf")
    
    print("\n📋 Development Commands:")
    print("  # Run tests")
    print("  cd packages/parser && python -m pytest")
    print("  cd packages/cli && npm test")
    print("  python tests/integration_test.py")
    
    print("  # Code quality")
    print("  cd packages/parser && black src/ tests/")
    print("  cd packages/parser && flake8 src/ tests/")
    print("  cd packages/cli && npm run lint")
    
    print("\n📁 Configuration:")
    print("  # Copy and customize sample config")
    print("  cp paper2data.sample.yml paper2data.yml")
    print("  # Edit paper2data.yml to your preferences")
    
    print("\n🔗 Useful Links:")
    print("  • Implementation Plan: Docs/Implementation.md")
    print("  • Project Structure: Docs/project_structure.md")
    print("  • UI/UX Design: Docs/UI_UX_doc.md")

def main():
    """Main setup function."""
    print("🚀 Paper2Data Development Environment Setup")
    print("="*50)
    
    # Check prerequisites
    if not check_prerequisites():
        print_status("Prerequisites check failed. Please install required tools:", "error")
        print("  • Python 3.10+: https://python.org/downloads")
        print("  • Node.js 16+: https://nodejs.org/downloads")
        print("  • npm (comes with Node.js)")
        print("  • Git: https://git-scm.com/downloads")
        sys.exit(1)
    
    try:
        # Setup environments
        python_exe, pip_exe, activate_script = setup_python_environment()
        setup_nodejs_environment()
        
        # Create sample config
        create_sample_config()
        
        # Run tests
        if not run_tests():
            print_status("Some tests failed, but setup is complete", "warning")
            print_status("You may need to check the installation", "warning")
        
        # Print instructions
        print_usage_instructions()
        
    except Exception as e:
        print_status(f"Setup failed: {str(e)}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main() 