"""
Pytest configuration and fixtures for Paper2Data tests.

This module provides shared fixtures, test utilities, and configuration
for the entire test suite.
"""

import pytest
import tempfile
import json
import time
import psutil
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, MagicMock

# Add source directories to path for testing
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "packages" / "parser" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "cli" / "src"))

# Import after path setup
try:
    from paper2data.extractor import (
        ContentExtractor, SectionExtractor, FigureExtractor, 
        TableExtractor, CitationExtractor
    )
    from paper2data.table_processor import TableProcessor
    from paper2data.utils import setup_logging, get_logger
except ImportError as e:
    pytest.skip(f"Could not import paper2data modules: {e}", allow_module_level=True)


# Test Data and Fixtures
# ======================

@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session") 
def sample_pdf_bytes():
    """Sample PDF content as bytes for testing."""
    # Create a minimal PDF-like structure for testing
    # This is a simplified mock - in real tests you'd have actual PDF bytes
    return b"%PDF-1.4\n%fake pdf content for testing\n%%EOF"


@pytest.fixture(scope="session")
def sample_table_text():
    """Sample table text for testing table extraction."""
    return """Method      Dataset    Accuracy   F1-Score   Time(s)
    SVM        MNIST      0.951      0.948      23.4
    RF         MNIST      0.963      0.961      45.2
    XGBoost    MNIST      0.987      0.985      67.8
    SVM        CIFAR-10   0.654      0.651      89.1
    RF         CIFAR-10   0.678      0.675      134.7
    XGBoost    CIFAR-10   0.701      0.698      201.3"""


@pytest.fixture(scope="session")
def sample_section_text():
    """Sample academic paper text with sections for testing."""
    return """
# Abstract

This paper presents a novel approach to machine learning that significantly
improves performance on benchmark datasets.

# Introduction

Machine learning has become increasingly important in recent years. Previous
work has shown that traditional approaches have limitations.

# Methodology

We propose a new algorithm that combines the benefits of supervised and
unsupervised learning approaches.

## Data Preprocessing

The data was preprocessed using standard techniques including normalization
and feature scaling.

## Model Architecture

Our model consists of three main components: feature extraction, classification,
and post-processing.

# Results

Experimental results demonstrate significant improvements over baseline methods.

# Conclusion

In conclusion, our approach shows promising results and opens new avenues
for future research.

# References

[1] Author, A. (2023). Previous Work on Machine Learning. Journal of AI, 15(3), 45-67.
[2] Researcher, R. (2022). Advances in Classification. Proc. ICML, 123-145.
"""


@pytest.fixture(scope="session")
def sample_citations():
    """Sample citations for testing citation extraction."""
    return [
        {
            "id": 1,
            "authors": ["Author, A.", "Collaborator, B."],
            "title": "Previous Work on Machine Learning",
            "journal": "Journal of AI",
            "year": "2023",
            "volume": "15",
            "issue": "3",
            "pages": "45-67"
        },
        {
            "id": 2,  
            "authors": ["Researcher, R."],
            "title": "Advances in Classification",
            "conference": "Proc. ICML",
            "year": "2022",
            "pages": "123-145"
        }
    ]


# Extractor Fixtures
# ==================

@pytest.fixture
def content_extractor(sample_pdf_bytes):
    """Content extractor instance for testing."""
    return ContentExtractor(sample_pdf_bytes)


@pytest.fixture
def section_extractor(sample_pdf_bytes):
    """Section extractor instance for testing."""
    return SectionExtractor(sample_pdf_bytes)


@pytest.fixture
def figure_extractor(sample_pdf_bytes):
    """Figure extractor instance for testing."""
    return FigureExtractor(sample_pdf_bytes)


@pytest.fixture
def table_extractor(sample_pdf_bytes):
    """Table extractor instance for testing."""
    return TableExtractor(sample_pdf_bytes)


@pytest.fixture
def citation_extractor(sample_pdf_bytes):
    """Citation extractor instance for testing."""
    return CitationExtractor(sample_pdf_bytes)


@pytest.fixture
def table_processor():
    """Table processor instance for testing."""
    return TableProcessor()


# Performance and Benchmarking Fixtures
# =====================================

@pytest.fixture
def performance_monitor():
    """Monitor for performance testing."""
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.start_memory = None
            self.end_memory = None
            self.process = psutil.Process()
        
        def start(self):
            """Start monitoring performance."""
            self.start_time = time.perf_counter()
            self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        def stop(self):
            """Stop monitoring and return metrics."""
            self.end_time = time.perf_counter()
            self.end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            return {
                'execution_time_seconds': self.end_time - self.start_time,
                'memory_used_mb': self.end_memory - self.start_memory,
                'peak_memory_mb': self.end_memory
            }
    
    return PerformanceMonitor()


@pytest.fixture
def benchmark_data():
    """Standard benchmark data for performance tests."""
    return {
        'small_document': "A" * 1000,      # 1KB
        'medium_document': "B" * 100000,   # 100KB  
        'large_document': "C" * 1000000,   # 1MB
        'complex_table': "\n".join([
            "Col1\tCol2\tCol3\tCol4\tCol5\tCol6\tCol7\tCol8\tCol9\tCol10"
        ] + [
            f"Row{i}\t{i}\t{i*2}\t{i*3}\t{i*4}\t{i*5}\t{i*6}\t{i*7}\t{i*8}\t{i*9}"
            for i in range(100)
        ])
    }


# File System Fixtures
# ====================

@pytest.fixture
def temp_output_dir():
    """Temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def golden_standards_dir():
    """Directory containing golden standard test outputs."""
    return Path(__file__).parent / "golden_standards"


# Mock Fixtures
# =============

@pytest.fixture
def mock_pdf_document():
    """Mock PyMuPDF document for testing without real PDFs."""
    mock_doc = Mock()
    mock_doc.page_count = 10
    mock_doc.metadata = {
        'title': 'Test Paper',
        'author': 'Test Author',
        'subject': 'Machine Learning',
        'creator': 'Test Creator'
    }
    
    # Mock pages
    mock_pages = []
    for i in range(10):
        mock_page = Mock()
        mock_page.number = i
        mock_page.get_text.return_value = f"Page {i+1} content with some test text."
        mock_page.get_images.return_value = []
        mock_pages.append(mock_page)
    
    mock_doc.__getitem__ = lambda self, idx: mock_pages[idx]
    mock_doc.__iter__ = lambda self: iter(mock_pages)
    
    return mock_doc


# Test Utilities
# ===============

@pytest.fixture
def assert_table_structure():
    """Utility function to assert table structure."""
    def _assert_table_structure(table_data: Dict[str, Any], 
                               expected_columns: int, 
                               expected_rows: int,
                               has_csv: bool = True):
        """Assert that table data has expected structure."""
        assert 'table_id' in table_data
        assert 'column_count' in table_data
        assert 'row_count' in table_data
        assert table_data['column_count'] == expected_columns
        assert table_data['row_count'] == expected_rows
        
        if has_csv:
            assert 'csv_content' in table_data
            assert 'format' in table_data
            assert table_data['format'] == 'csv'
    
    return _assert_table_structure


@pytest.fixture
def assert_extraction_quality():
    """Utility function to assert extraction quality."""
    def _assert_extraction_quality(results: Dict[str, Any], 
                                 min_sections: int = 1,
                                 min_confidence: float = 0.5):
        """Assert that extraction results meet quality standards."""
        if 'sections' in results:
            sections = results['sections']
            if isinstance(sections, dict) and 'sections' in sections:
                assert len(sections['sections']) >= min_sections
        
        if 'tables' in results:
            tables = results['tables']
            if isinstance(tables, dict) and 'tables' in tables:
                for table in tables['tables']:
                    if 'confidence' in table:
                        assert table['confidence'] >= min_confidence
    
    return _assert_extraction_quality


# Logging Setup for Tests
# =======================

@pytest.fixture(scope="session", autouse=True)
def setup_test_logging():
    """Set up logging for test sessions."""
    try:
        setup_logging(level="DEBUG")
        logger = get_logger()
        logger.info("Test session started")
    except Exception:
        # Fallback if setup_logging is not working
        import logging
        logging.basicConfig(level=logging.DEBUG)


# Pytest Hooks
# =============

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Ensure test data directory exists
    test_data_dir = Path(__file__).parent / "data"
    test_data_dir.mkdir(exist_ok=True)
    
    # Ensure golden standards directory exists
    golden_dir = Path(__file__).parent / "golden_standards"
    golden_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add automatic markers."""
    for item in items:
        # Mark slow tests
        if "slow" in item.keywords or any(marker in item.name.lower() 
                                         for marker in ["performance", "benchmark"]):
            item.add_marker(pytest.mark.slow)
        
        # Mark tests requiring external resources
        if any(keyword in item.name.lower() for keyword in ["pdf", "file"]):
            item.add_marker(pytest.mark.requires_pdf)
        
        if any(keyword in item.name.lower() for keyword in ["url", "download", "arxiv"]):
            item.add_marker(pytest.mark.requires_network)


def pytest_report_header(config):
    """Add custom header to pytest report."""
    return [
        "Paper2Data Test Suite",
        f"Python: {sys.version}",
        f"Working Directory: {os.getcwd()}",
        f"Test Data Directory: {Path(__file__).parent / 'data'}",
    ] 