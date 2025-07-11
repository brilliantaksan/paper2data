"""
Paper2Data Parser Package

A Python package for extracting and parsing content from academic papers.
Supports PDF files, arXiv URLs, and DOI resolution.
"""

__version__ = "1.0.0"
__author__ = "Paper2Data Team"
__email__ = "team@paper2data.dev"

# Main API exports
from .ingest import PDFIngestor, URLIngestor, DOIIngestor
from .extractor import ContentExtractor, SectionExtractor, FigureExtractor, TableExtractor
from .utils import setup_logging, validate_input, format_output

__all__ = [
    "PDFIngestor",
    "URLIngestor", 
    "DOIIngestor",
    "ContentExtractor",
    "SectionExtractor",
    "FigureExtractor",
    "TableExtractor",
    "setup_logging",
    "validate_input",
    "format_output",
] 