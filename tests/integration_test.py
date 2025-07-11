#!/usr/bin/env python3
"""
Integration tests for Paper2Data parser package.

Tests the overall package structure and cross-module integration.
"""

import sys
import pytest
from pathlib import Path

# Add the parser package to the path for testing
parser_src = Path(__file__).parent.parent / "packages" / "parser" / "src"
sys.path.insert(0, str(parser_src))

def test_package_imports():
    """Test that all main package modules can be imported."""
    try:
        # Test individual module imports
        import ingest
        import extractor
        import utils
        
        print("✅ All parser modules imported successfully")
        
        # Test that classes can be instantiated
        pdf_ingestor = ingest.PDFIngestor("test.pdf")
        content_extractor = extractor.ContentExtractor(b"test content")
        
        assert pdf_ingestor is not None
        assert content_extractor is not None
        
        print("✅ Parser classes can be instantiated")
        
    except ImportError as e:
        pytest.fail(f"Failed to import parser modules: {e}")


def test_package_structure():
    """Test that the package structure is correct."""
    parser_dir = Path(__file__).parent.parent / "packages" / "parser"
    
    # Check required files exist
    required_files = [
        "src/__init__.py",
        "src/ingest.py", 
        "src/extractor.py",
        "src/utils.py",
        "tests/test_parser.py",
        "pyproject.toml"
    ]
    
    for file_path in required_files:
        full_path = parser_dir / file_path
        assert full_path.exists(), f"Required file missing: {file_path}"
    
    print("✅ Parser package structure is correct")


def test_placeholder_functionality():
    """Test that placeholder methods raise NotImplementedError as expected."""
    import ingest
    import extractor
    import utils
    
    # Test ingest placeholders
    pdf_ingestor = ingest.PDFIngestor("test.pdf")
    with pytest.raises(NotImplementedError):
        pdf_ingestor.validate()
    with pytest.raises(NotImplementedError):
        pdf_ingestor.ingest()
    
    # Test extractor placeholders
    content_extractor = extractor.ContentExtractor(b"test")
    with pytest.raises(NotImplementedError):
        content_extractor.extract()
    
    # Test utils placeholders
    with pytest.raises(NotImplementedError):
        utils.setup_logging()
    
    print("✅ Placeholder functionality works as expected")


def test_configuration_files():
    """Test that configuration files are properly formatted."""
    parser_dir = Path(__file__).parent.parent / "packages" / "parser"
    
    # Test pyproject.toml exists and has basic structure
    pyproject_file = parser_dir / "pyproject.toml"
    assert pyproject_file.exists(), "pyproject.toml is missing"
    
    content = pyproject_file.read_text()
    assert "[build-system]" in content
    assert "[project]" in content
    assert "paper2data-parser" in content
    
    print("✅ Configuration files are properly formatted")


def test_development_readiness():
    """Test that the package is ready for development."""
    parser_dir = Path(__file__).parent.parent / "packages" / "parser"
    
    # Check that we can run tests
    test_file = parser_dir / "tests" / "test_parser.py"
    assert test_file.exists(), "Test file is missing"
    
    # Check that the package structure supports future development
    src_dir = parser_dir / "src"
    assert src_dir.exists(), "Source directory is missing"
    
    required_modules = ["ingest.py", "extractor.py", "utils.py"]
    for module in required_modules:
        module_path = src_dir / module
        assert module_path.exists(), f"Required module missing: {module}"
        
        # Check that each module has content
        content = module_path.read_text()
        assert len(content) > 100, f"Module {module} appears to be empty"
        assert "NotImplementedError" in content, f"Module {module} missing placeholder implementations"
    
    print("✅ Package is ready for development")


if __name__ == "__main__":
    print("🧪 Running Paper2Data Parser Integration Tests")
    print("=" * 50)
    
    try:
        test_package_imports()
        test_package_structure() 
        test_placeholder_functionality()
        test_configuration_files()
        test_development_readiness()
        
        print("\n" + "=" * 50)
        print("✅ All integration tests passed!")
        print("🚀 Parser package is ready for Stage 1 development")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        sys.exit(1) 