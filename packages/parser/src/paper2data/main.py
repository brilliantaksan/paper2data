#!/usr/bin/env python3
"""
Paper2Data Parser - Command Line Interface

Main entry point for the Python parser that can be called from the Node.js CLI.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from . import (
    create_ingestor, 
    extract_all_content,
    setup_logging, 
    get_logger,
    load_config,
    save_json,
    create_output_structure,
    format_output,
    ValidationError,
    ProcessingError,
    ConfigurationError
)


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Paper2Data Parser - Extract content from academic papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m paper2data.parser convert paper.pdf
  python -m paper2data.parser convert https://arxiv.org/abs/2301.00001
  python -m paper2data.parser convert 10.1038/nature12373 --output ./output
        """
    )
    
    parser.add_argument(
        "command",
        choices=["convert", "validate", "info"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "input",
        help="Input source: PDF file path, arXiv URL, or DOI"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (default: ./paper2data_output)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["json", "yaml", "markdown"],
        default="json",
        help="Output format for metadata (default: json)"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Configuration file path"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Log file path"
    )
    
    parser.add_argument(
        "--no-figures",
        action="store_true",
        help="Skip figure extraction"
    )
    
    parser.add_argument(
        "--no-tables",
        action="store_true", 
        help="Skip table extraction"
    )
    
    parser.add_argument(
        "--no-citations",
        action="store_true",
        help="Skip citation extraction"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate input without processing"
    )
    
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON to stdout (for CLI integration)"
    )
    
    return parser


def validate_input_command(input_source: str, args: argparse.Namespace) -> Dict[str, Any]:
    """Validate input source and return validation results."""
    logger = get_logger()
    
    try:
        ingestor = create_ingestor(input_source)
        is_valid = ingestor.validate()
        
        result = {
            "valid": is_valid,
            "input_source": input_source,
            "metadata": ingestor.metadata,
            "message": "Input validation successful"
        }
        
        logger.info(f"Validation successful for: {input_source}")
        return result
        
    except (ValidationError, ProcessingError) as e:
        result = {
            "valid": False,
            "input_source": input_source,
            "error": str(e),
            "message": "Input validation failed"
        }
        
        logger.error(f"Validation failed: {str(e)}")
        return result


def info_command(input_source: str, args: argparse.Namespace) -> Dict[str, Any]:
    """Get information about input source without full processing."""
    logger = get_logger()
    
    try:
        # Validate first
        validation_result = validate_input_command(input_source, args)
        if not validation_result["valid"]:
            return validation_result
        
        # For PDF files, get basic info
        ingestor = create_ingestor(input_source)
        ingestor.validate()  # This populates metadata
        
        result = {
            "input_source": input_source,
            "metadata": ingestor.metadata,
            "estimated_processing_time": "1-5 minutes (depends on document size)",
            "supported_operations": ["text extraction", "section detection", "figure extraction", "table detection", "citation extraction"]
        }
        
        logger.info(f"Info retrieved for: {input_source}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to get info: {str(e)}")
        return {
            "error": str(e),
            "message": "Failed to retrieve information"
        }


def convert_command(input_source: str, args: argparse.Namespace, config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert paper to structured data."""
    logger = get_logger()
    
    try:
        # Create ingestor and validate
        logger.info(f"Starting conversion of: {input_source}")
        ingestor = create_ingestor(input_source)
        ingestor.validate()
        
        if args.dry_run:
            return {
                "success": True,
                "input_source": input_source,
                "message": "Dry run completed - input is valid",
                "metadata": ingestor.metadata
            }
        
        # Ingest content
        logger.info("Ingesting content...")
        pdf_content = ingestor.ingest()
        
        # Extract all content
        logger.info("Extracting content...")
        extraction_results = extract_all_content(pdf_content)
        
        # Determine output directory
        if args.output:
            output_dir = args.output
        else:
            output_dir = Path(config.get("output", {}).get("directory", "./paper2data_output"))
        
        # Create output structure
        paper_title = extraction_results.get("content", {}).get("metadata", {}).get("title", "unknown")
        if not paper_title or paper_title == "unknown":
            # Try to get title from filename or URL
            if input_source.endswith('.pdf'):
                paper_title = Path(input_source).stem
            else:
                paper_title = "unknown_paper"
        
        output_structure = create_output_structure(output_dir, paper_title)
        
        # Save extracted content
        logger.info("Saving extracted content...")
        
        # Save metadata
        metadata_file = output_structure["metadata"] / "document_info.json"
        save_json(extraction_results.get("content", {}).get("metadata", {}), metadata_file)
        
        # Save sections
        sections = extraction_results.get("sections", {}).get("sections", {})
        for section_name, section_content in sections.items():
            if section_content:
                section_file = output_structure["sections"] / f"{section_name}.md"
                with open(section_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {section_name.title()}\n\n{section_content}")
        
        # Save figures (if enabled)
        if not args.no_figures and config.get("processing", {}).get("extract_figures", True):
            figures = extraction_results.get("figures", {}).get("figures", [])
            for figure in figures:
                figure_file = output_structure["figures"] / f"{figure['figure_id']}.png"
                with open(figure_file, 'wb') as f:
                    f.write(figure["data"])
        
        # Save tables (if enabled)
        if not args.no_tables and config.get("processing", {}).get("extract_tables", True):
            tables = extraction_results.get("tables", {}).get("tables", [])
            for table in tables:
                # Use CSV format if available, otherwise fall back to raw text
                if 'csv_content' in table and table['csv_content']:
                    table_file = output_structure["tables"] / f"{table['table_id']}.csv"
                    with open(table_file, 'w', encoding='utf-8', newline='') as f:
                        f.write(table["csv_content"])
                else:
                    # Fallback to raw text format
                    table_file = output_structure["tables"] / f"{table['table_id']}.txt"
                    with open(table_file, 'w', encoding='utf-8') as f:
                        f.write(table["raw_text"])
        
        # Save citations (if enabled)
        if not args.no_citations and config.get("processing", {}).get("extract_citations", True):
            citations = extraction_results.get("citations", {}).get("reference_list", [])
            if citations:
                citations_file = output_structure["metadata"] / "citations.json"
                save_json({"references": citations}, citations_file)
        
        # Save comprehensive results (excluding binary data)
        results_file = output_structure["root"] / "extraction_results.json"
        json_safe_results = {
            "content": extraction_results.get("content", {}),
            "sections": extraction_results.get("sections", {}),
            "tables": extraction_results.get("tables", {}),
            "citations": extraction_results.get("citations", {}),
            "summary": extraction_results.get("summary", {}),
            "extraction_timestamp": extraction_results.get("extraction_timestamp", ""),
            # Note: Figure binary data is saved separately as PNG files
            "figures": {
                "summary": extraction_results.get("figures", {}).get("summary", {}),
                "figure_count": len(extraction_results.get("figures", {}).get("figures", []))
            }
        }
        save_json(json_safe_results, results_file)
        
        # Create README
        readme_file = output_structure["root"] / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"""# {paper_title}

## Extraction Summary

- **Pages**: {extraction_results.get('summary', {}).get('total_pages', 'Unknown')}
- **Words**: {extraction_results.get('summary', {}).get('total_words', 'Unknown')}
- **Sections**: {extraction_results.get('summary', {}).get('sections_found', 0)}
- **Figures**: {extraction_results.get('summary', {}).get('figures_found', 0)}
- **Tables**: {extraction_results.get('summary', {}).get('tables_found', 0)}
- **References**: {extraction_results.get('summary', {}).get('references_found', 0)}

## Directory Structure

- `sections/` - Document sections in Markdown format
- `figures/` - Extracted figures as PNG files
- `tables/` - Extracted tables as CSV files (structured data) or text files (fallback)
- `metadata/` - Document metadata and citations
- `extraction_results.json` - Complete extraction results

## Source

Original source: {input_source}
Processed on: {extraction_results.get('extraction_timestamp', 'Unknown')}
""")
        
        result = {
            "success": True,
            "input_source": input_source,
            "output_directory": str(output_structure["root"]),
            "summary": extraction_results.get("summary", {}),
            "files_created": {
                "sections": len(sections),
                "figures": len(extraction_results.get("figures", {}).get("figures", [])),
                "tables": len(extraction_results.get("tables", {}).get("tables", [])),
                "metadata_files": 2  # document_info.json + citations.json
            }
        }
        
        logger.info(f"Conversion completed successfully: {output_structure['root']}")
        return result
        
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        return {
            "success": False,
            "input_source": input_source,
            "error": str(e),
            "message": "Conversion failed"
        }


def main() -> int:
    """Main entry point."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Set up logging - use stderr when JSON output is requested
        log_level = args.log_level or config.get("logging", {}).get("level", "INFO")
        log_file = args.log_file or config.get("logging", {}).get("file")
        
        # Use stderr for logging when JSON output is requested to keep stdout clean
        if args.json_output:
            import sys
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(getattr(logging, log_level.upper()))
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            
            logger = logging.getLogger("paper2data.parser")
            logger.setLevel(getattr(logging, log_level.upper()))
            logger.handlers.clear()
            logger.addHandler(console_handler)
            
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(getattr(logging, log_level.upper()))
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        else:
            setup_logging(level=log_level, log_file=log_file)
        
        logger = get_logger()
        logger.info(f"Starting Paper2Data parser - Command: {args.command}")
        
        # Execute command
        if args.command == "validate":
            result = validate_input_command(args.input, args)
        elif args.command == "info":
            result = info_command(args.input, args)
        elif args.command == "convert":
            result = convert_command(args.input, args, config)
        else:
            result = {"error": f"Unknown command: {args.command}"}
        
        # Output results
        if args.json_output:
            print(json.dumps(result, indent=2))
        else:
            if result.get("success", False) or result.get("valid", False):
                print("✅ Operation completed successfully")
                if "output_directory" in result:
                    print(f"📂 Output: {result['output_directory']}")
                if "summary" in result:
                    summary = result["summary"]
                    print(f"📄 {summary.get('total_pages', 0)} pages, {summary.get('total_words', 0)} words")
                    print(f"📊 {summary.get('sections_found', 0)} sections, {summary.get('figures_found', 0)} figures, {summary.get('tables_found', 0)} tables")
            else:
                print("❌ Operation failed")
                if "error" in result:
                    print(f"Error: {result['error']}")
        
        return 0 if result.get("success", result.get("valid", False)) else 1
        
    except Exception as e:
        if args.json_output:
            print(json.dumps({"error": str(e), "success": False}, indent=2))
        else:
            print(f"❌ Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 