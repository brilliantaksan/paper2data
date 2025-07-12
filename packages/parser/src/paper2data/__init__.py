"""
Paper2Data Parser Package

A Python package for extracting and parsing content from academic papers.
Supports PDF files, arXiv URLs, and DOI resolution.
"""

__version__ = "1.0.0"
__author__ = "Paper2Data Team"
__email__ = "team@paper2data.dev"

# Main API exports
from .ingest import PDFIngestor, URLIngestor, DOIIngestor, create_ingestor
from .extractor import (
    ContentExtractor, 
    SectionExtractor, 
    FigureExtractor, 
    TableExtractor, 
    CitationExtractor,
    extract_all_content
)
from .api_integration import (
    ArxivAPIClient,
    DOIAPIClient,
    BatchProcessor,
    arxiv_client,
    doi_client,
    batch_processor,
    api_cache
)
from .utils import (
    setup_logging, 
    get_logger,
    validate_input, 
    format_output, 
    clean_text,
    load_config,
    save_json,
    ensure_directory,
    create_output_structure,
    progress_callback,
    suppress_stderr,
    normalize_url,
    normalize_arxiv_url,
    normalize_doi,
    validate_arxiv_id,
    validate_doi,
    extract_identifiers_from_text,
    validate_url_accessibility,
    ProcessingError,
    ValidationError,
    ConfigurationError
)

__all__ = [
    # Ingestors
    "PDFIngestor",
    "URLIngestor", 
    "DOIIngestor",
    "create_ingestor",
    
    # Extractors
    "ContentExtractor",
    "SectionExtractor",
    "FigureExtractor",
    "TableExtractor",
    "CitationExtractor",
    "extract_all_content",
    
    # API Integration
    "ArxivAPIClient",
    "DOIAPIClient",
    "BatchProcessor",
    "arxiv_client",
    "doi_client",
    "batch_processor",
    "api_cache",
    
    # Utilities
    "setup_logging",
    "get_logger", 
    "validate_input",
    "format_output",
    "clean_text",
    "load_config",
    "save_json",
    "ensure_directory", 
    "create_output_structure",
    "progress_callback",
    "suppress_stderr",
    "normalize_url",
    "normalize_arxiv_url",
    "normalize_doi",
    "validate_arxiv_id",
    "validate_doi",
    "extract_identifiers_from_text",
    "validate_url_accessibility",
    
    # Exceptions
    "ProcessingError",
    "ValidationError",
    "ConfigurationError",
]

# Package metadata
SUPPORTED_FORMATS = ["pdf"]
SUPPORTED_SOURCES = ["file", "url", "arxiv", "doi"]
DEFAULT_CONFIG = {
    "output": {
        "format": "json",
        "directory": "./paper2data_output",
        "preserve_structure": True
    },
    "processing": {
        "extract_figures": True,
        "extract_tables": True,
        "extract_citations": True,
        "max_file_size_mb": 100
    },
    "logging": {
        "level": "INFO",
        "file": None
    }
} 