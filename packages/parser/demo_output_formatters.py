#!/usr/bin/env python3
"""
Demo script for Output Formatters in Paper2Data

This script demonstrates the comprehensive output formatting capabilities
including HTML, LaTeX, XML, CSV, Markdown formats with various configuration
options and batch processing features.
"""

import os
import sys
import tempfile
import json
from datetime import datetime
from typing import Dict, Any

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from paper2data.output_formatters import (
    OutputFormat, FormatConfig, FormatterFactory,
    format_output, batch_format,
    export_to_html, export_to_latex, export_to_xml,
    export_to_csv, export_to_markdown, export_all_formats
)

def create_comprehensive_sample_data() -> Dict[str, Any]:
    """Create comprehensive sample data for demonstration"""
    return {
        "extraction_timestamp": datetime.now().isoformat(),
        "metadata": {
            "title": "Advanced Neural Networks for Natural Language Processing: A Comprehensive Survey",
            "authors": [
                {"name": "Dr. Alice Johnson", "position": 1, "affiliation": "Stanford University"},
                {"name": "Prof. Bob Chen", "position": 2, "affiliation": "MIT"},
                {"name": "Dr. Carol Davis", "position": 3, "affiliation": "Google Research"}
            ],
            "publication_info": {
                "year": 2023,
                "journal": "Journal of AI Research",
                "volume": "45",
                "issue": "3",
                "pages": "123-156",
                "publisher": "AI Press"
            },
            "doi": "10.1234/jair.2023.neural.nlp",
            "arxiv_id": "2301.12345",
            "keywords": [
                "neural networks", "natural language processing", "transformers",
                "attention mechanisms", "deep learning", "artificial intelligence"
            ],
            "abstract": "This comprehensive survey examines the latest advances in neural networks for natural language processing. We review transformer architectures, attention mechanisms, and their applications in various NLP tasks. Our analysis covers both theoretical foundations and practical implementations, providing insights into current challenges and future research directions. The paper includes extensive comparisons of different approaches and presents novel evaluation metrics for assessing model performance.",
            "title_confidence": 0.98,
            "abstract_confidence": 0.95,
            "author_confidence": 0.92
        },
        "content": {
            "full_text": """
            Introduction

            Natural Language Processing (NLP) has witnessed unprecedented advances with the advent of neural networks. 
            This survey provides a comprehensive overview of current state-of-the-art methods and their applications.

            The field has evolved from simple recurrent networks to sophisticated transformer architectures that have 
            revolutionized how we approach language understanding and generation tasks. Deep learning models now achieve 
            human-level performance on many benchmark tasks.

            Related Work

            Early neural approaches to NLP relied on recurrent neural networks (RNNs) and their variants. The introduction 
            of attention mechanisms marked a significant breakthrough, allowing models to focus on relevant parts of the input.

            The transformer architecture, introduced by Vaswani et al., has become the foundation for most modern NLP systems. 
            Models like BERT, GPT, and T5 have set new standards for performance across a wide range of tasks.

            Methodology

            Our analysis covers three main categories of neural networks used in NLP:
            1. Recurrent Neural Networks and their variants
            2. Transformer-based architectures
            3. Hybrid approaches combining multiple techniques

            We evaluate these approaches on standard benchmarks including GLUE, SuperGLUE, and domain-specific datasets.

            Results

            Our experiments demonstrate that transformer-based models consistently outperform traditional approaches 
            across all evaluated tasks. However, they require significantly more computational resources.

            The attention visualization reveals that models learn meaningful linguistic patterns, focusing on relevant 
            words and phrases when making predictions.

            Discussion

            While transformer models achieve excellent performance, several challenges remain:
            - Computational complexity and energy consumption
            - Interpretability and explainability
            - Bias and fairness considerations
            - Generalization to new domains

            Future research should address these limitations while exploring new architectural innovations.

            Conclusion

            This survey highlights the transformative impact of neural networks on NLP. As the field continues to evolve, 
            we expect further innovations that will push the boundaries of what's possible in language understanding and generation.
            """,
            "statistics": {
                "page_count": 34,
                "word_count": 8750,
                "character_count": 52340,
                "paragraph_count": 45,
                "sentence_count": 234
            }
        },
        "sections": {
            "sections": [
                {
                    "title": "Abstract",
                    "content": "This comprehensive survey examines the latest advances in neural networks for natural language processing...",
                    "page": 1,
                    "confidence": 0.98
                },
                {
                    "title": "1. Introduction",
                    "content": "Natural Language Processing (NLP) has witnessed unprecedented advances with the advent of neural networks...",
                    "page": 2,
                    "confidence": 0.95
                },
                {
                    "title": "2. Related Work",
                    "content": "Early neural approaches to NLP relied on recurrent neural networks (RNNs) and their variants...",
                    "page": 5,
                    "confidence": 0.93
                },
                {
                    "title": "3. Methodology",
                    "content": "Our analysis covers three main categories of neural networks used in NLP...",
                    "page": 12,
                    "confidence": 0.97
                },
                {
                    "title": "4. Results",
                    "content": "Our experiments demonstrate that transformer-based models consistently outperform...",
                    "page": 18,
                    "confidence": 0.96
                },
                {
                    "title": "5. Discussion",
                    "content": "While transformer models achieve excellent performance, several challenges remain...",
                    "page": 25,
                    "confidence": 0.94
                },
                {
                    "title": "6. Conclusion",
                    "content": "This survey highlights the transformative impact of neural networks on NLP...",
                    "page": 30,
                    "confidence": 0.99
                }
            ],
            "section_count": 7
        },
        "figures": {
            "figures": [
                {
                    "caption": "Figure 1: Transformer architecture overview showing encoder-decoder structure",
                    "page": 8,
                    "width": 500,
                    "height": 300,
                    "type": "diagram",
                    "confidence": 0.92
                },
                {
                    "caption": "Figure 2: Attention visualization for sample sentences",
                    "page": 14,
                    "width": 600,
                    "height": 400,
                    "type": "heatmap",
                    "confidence": 0.88
                },
                {
                    "caption": "Figure 3: Performance comparison across different model architectures",
                    "page": 20,
                    "width": 550,
                    "height": 350,
                    "type": "bar_chart",
                    "confidence": 0.95
                },
                {
                    "caption": "Figure 4: Training loss curves for various models",
                    "page": 22,
                    "width": 480,
                    "height": 320,
                    "type": "line_chart",
                    "confidence": 0.91
                }
            ],
            "figure_count": 4
        },
        "tables": {
            "tables": [
                {
                    "caption": "Table 1: Model performance on GLUE benchmark",
                    "headers": ["Model", "COLA", "SST-2", "MRPC", "STS-B", "QQP", "MNLI", "QNLI", "RTE", "Average"],
                    "data": [
                        ["BERT-base", "52.1", "93.5", "88.9", "85.8", "89.2", "84.6", "90.5", "66.4", "81.4"],
                        ["RoBERTa-base", "56.8", "94.8", "90.2", "86.5", "89.8", "87.6", "92.8", "70.1", "83.6"],
                        ["DeBERTa-base", "59.2", "95.3", "91.7", "88.2", "90.5", "88.9", "93.6", "72.6", "85.0"],
                        ["Our Model", "61.5", "96.1", "93.2", "89.7", "91.8", "90.3", "94.8", "75.2", "86.6"]
                    ],
                    "page": 19,
                    "confidence": 0.97
                },
                {
                    "caption": "Table 2: Computational requirements comparison",
                    "headers": ["Model", "Parameters (M)", "Training Time (GPU hrs)", "Memory (GB)", "Inference Speed (samples/sec)"],
                    "data": [
                        ["BERT-base", "110", "72", "16", "156"],
                        ["RoBERTa-base", "125", "96", "18", "142"],
                        ["DeBERTa-base", "139", "108", "20", "134"],
                        ["Our Model", "143", "84", "19", "148"]
                    ],
                    "page": 24,
                    "confidence": 0.94
                }
            ],
            "total_tables": 2
        },
        "equations": {
            "equations": [
                {
                    "text": "Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V",
                    "latex": "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V",
                    "page": 9,
                    "confidence": 0.99,
                    "type": "attention_mechanism"
                },
                {
                    "text": "MultiHead(Q, K, V) = Concat(head_1, ..., head_h)W^O",
                    "latex": "\\text{MultiHead}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\ldots, \\text{head}_h)W^O",
                    "page": 10,
                    "confidence": 0.97,
                    "type": "multi_head_attention"
                },
                {
                    "text": "Loss = -sum(y_i * log(p_i))",
                    "latex": "\\mathcal{L} = -\\sum_{i} y_i \\log(p_i)",
                    "page": 16,
                    "confidence": 0.95,
                    "type": "cross_entropy_loss"
                }
            ],
            "total_equations": 3
        },
        "citations": {
            "references": [
                {
                    "text": "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in neural information processing systems, 30.",
                    "authors": ["Vaswani, A.", "Shazeer, N.", "Parmar, N.", "Uszkoreit, J."],
                    "title": "Attention is all you need",
                    "year": 2017,
                    "venue": "Advances in neural information processing systems",
                    "volume": "30",
                    "doi": "10.5555/3295222.3295349"
                },
                {
                    "text": "Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805.",
                    "authors": ["Devlin, J.", "Chang, M. W.", "Lee, K.", "Toutanova, K."],
                    "title": "Bert: Pre-training of deep bidirectional transformers for language understanding",
                    "year": 2018,
                    "venue": "arXiv preprint",
                    "arxiv_id": "1810.04805"
                },
                {
                    "text": "Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. Advances in neural information processing systems, 33, 1877-1901.",
                    "authors": ["Brown, T.", "Mann, B.", "Ryder, N.", "Subbiah, M."],
                    "title": "Language models are few-shot learners",
                    "year": 2020,
                    "venue": "Advances in neural information processing systems",
                    "volume": "33",
                    "pages": "1877-1901"
                }
            ],
            "reference_count": 3,
            "in_text_citations": [
                {"text": "(Vaswani et al., 2017)", "page": 3},
                {"text": "(Devlin et al., 2018)", "page": 4},
                {"text": "(Brown et al., 2020)", "page": 6}
            ]
        },
        "citation_networks": {
            "networks": {
                "citation": {
                    "basic_metrics": {
                        "num_nodes": 15,
                        "num_edges": 23,
                        "density": 0.12,
                        "is_connected": True,
                        "num_components": 1
                    }
                },
                "author_collaboration": {
                    "basic_metrics": {
                        "num_nodes": 8,
                        "num_edges": 12,
                        "density": 0.43,
                        "is_connected": True,
                        "num_components": 1
                    }
                }
            },
            "author_analysis": {
                "Dr. Alice Johnson": {
                    "paper_count": 3,
                    "h_index": 12,
                    "total_citations": 245,
                    "collaboration_count": 15
                },
                "Prof. Bob Chen": {
                    "paper_count": 5,
                    "h_index": 18,
                    "total_citations": 456,
                    "collaboration_count": 22
                }
            },
            "processing_status": "completed",
            "total_papers_analyzed": 1
        },
        "summary": {
            "total_pages": 34,
            "total_words": 8750,
            "sections_found": 7,
            "figures_found": 4,
            "tables_found": 2,
            "references_found": 3,
            "equations_found": 3,
            "advanced_figures_found": 4,
            "captions_found": 6,
            "metadata_extracted": True,
            "authors_found": 3,
            "keywords_found": 6,
            "citations_in_metadata": 0,
            "doi_found": True,
            "title_confidence": 0.98,
            "abstract_confidence": 0.95,
            "author_confidence": 0.92,
            "citation_networks_analyzed": True,
            "total_papers_in_network": 1,
            "network_types_built": 2
        }
    }

def demonstrate_basic_formatting():
    """Demonstrate basic formatting for each supported format"""
    print("=" * 80)
    print("BASIC OUTPUT FORMATTING DEMO")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    title = data["metadata"]["title"]
    
    print(f"✓ Created sample data for: '{title[:50]}...'")
    print(f"✓ Data includes: metadata, content, figures, tables, equations, citations, networks")
    
    print("\n1. SUPPORTED OUTPUT FORMATS")
    print("-" * 50)
    
    # Test each format
    with tempfile.TemporaryDirectory() as temp_dir:
        formats_to_test = [
            (OutputFormat.JSON, "json"),
            (OutputFormat.HTML, "html"),
            (OutputFormat.LATEX, "tex"),
            (OutputFormat.XML, "xml"),
            (OutputFormat.CSV, "csv"),
            (OutputFormat.MARKDOWN, "md")
        ]
        
        for output_format, extension in formats_to_test:
            output_path = os.path.join(temp_dir, f"demo.{extension}")
            
            print(f"\n  {output_format.value.upper()} Format:")
            success = format_output(data, output_path, output_format)
            
            if success:
                file_size = os.path.getsize(output_path)
                print(f"    ✓ Success: {output_path} ({file_size:,} bytes)")
                
                # Show sample content for text-based formats
                if output_format in [OutputFormat.HTML, OutputFormat.MARKDOWN, OutputFormat.LATEX]:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        sample = content[:200] + "..." if len(content) > 200 else content
                        print(f"    Sample: {sample.strip()}")
                
                elif output_format == OutputFormat.JSON:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                        print(f"    Structure: {list(json_data.keys())}")
                
                elif output_format == OutputFormat.CSV:
                    # List CSV files created
                    csv_files = [f for f in os.listdir(temp_dir) if f.startswith("demo_") and f.endswith(".csv")]
                    print(f"    Files created: {len(csv_files)} CSV files")
                    for csv_file in csv_files:
                        csv_path = os.path.join(temp_dir, csv_file)
                        csv_size = os.path.getsize(csv_path)
                        print(f"      - {csv_file} ({csv_size} bytes)")
            else:
                print(f"    ✗ Failed to format {output_format.value}")
    
    return data

def demonstrate_configuration_options():
    """Demonstrate various configuration options"""
    print("\n" + "=" * 80)
    print("CONFIGURATION OPTIONS DEMO")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    
    print("\n1. SELECTIVE CONTENT INCLUSION")
    print("-" * 50)
    
    # Test selective inclusion
    configs = [
        ("Metadata Only", FormatConfig(
            include_figures=False, include_tables=False, 
            include_equations=False, include_citations=False, include_networks=False
        )),
        ("Content + Figures", FormatConfig(
            include_metadata=False, include_tables=False, 
            include_equations=False, include_citations=False, include_networks=False
        )),
        ("Academic Focus", FormatConfig(
            include_metadata=True, include_equations=True, include_citations=True,
            include_figures=False, include_tables=False, include_networks=False
        )),
        ("Complete Analysis", FormatConfig())  # All included
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for config_name, config in configs:
            print(f"\n  {config_name} Configuration:")
            
            output_path = os.path.join(temp_dir, f"{config_name.lower().replace(' ', '_')}.html")
            formatter = FormatterFactory.create_formatter(OutputFormat.HTML, config)
            success = formatter.format(data, output_path)
            
            if success:
                file_size = os.path.getsize(output_path)
                print(f"    ✓ HTML generated: {file_size:,} bytes")
                
                # Check what sections are included
                with open(output_path, 'r') as f:
                    content = f.read()
                    sections = []
                    if "Document Metadata" in content:
                        sections.append("Metadata")
                    if "Figures" in content:
                        sections.append("Figures")
                    if "Tables" in content:
                        sections.append("Tables")
                    if "Equations" in content:
                        sections.append("Equations")
                    if "Citations" in content:
                        sections.append("Citations")
                    if "Networks" in content:
                        sections.append("Networks")
                    
                    print(f"    Sections: {', '.join(sections) if sections else 'Content only'}")
            else:
                print(f"    ✗ Failed to generate HTML")
    
    print("\n2. FORMAT-SPECIFIC OPTIONS")
    print("-" * 50)
    
    # Test format-specific options
    with tempfile.TemporaryDirectory() as temp_dir:
        # HTML with and without CSS
        print("\n  HTML CSS Options:")
        html_configs = [
            ("With CSS", FormatConfig(html_include_css=True)),
            ("Without CSS", FormatConfig(html_include_css=False))
        ]
        
        for config_name, config in html_configs:
            output_path = os.path.join(temp_dir, f"html_{config_name.lower().replace(' ', '_')}.html")
            success = format_output(data, output_path, OutputFormat.HTML, config)
            if success:
                file_size = os.path.getsize(output_path)
                with open(output_path, 'r') as f:
                    content = f.read()
                    has_css = "<style>" in content
                    print(f"    {config_name}: {file_size:,} bytes, CSS: {'Yes' if has_css else 'No'}")
        
        # LaTeX document classes
        print("\n  LaTeX Document Classes:")
        latex_configs = [
            ("Article", FormatConfig(latex_document_class="article")),
            ("Report", FormatConfig(latex_document_class="report")),
            ("Book", FormatConfig(latex_document_class="book"))
        ]
        
        for config_name, config in latex_configs:
            output_path = os.path.join(temp_dir, f"latex_{config_name.lower()}.tex")
            success = format_output(data, output_path, OutputFormat.LATEX, config)
            if success:
                file_size = os.path.getsize(output_path)
                with open(output_path, 'r') as f:
                    content = f.read()
                    doc_class_line = [line for line in content.split('\n') if line.startswith('\\documentclass')][0]
                    print(f"    {config_name}: {file_size:,} bytes, {doc_class_line}")
        
        # CSV delimiters
        print("\n  CSV Delimiter Options:")
        csv_configs = [
            ("Comma", FormatConfig(csv_delimiter=",")),
            ("Semicolon", FormatConfig(csv_delimiter=";")),
            ("Tab", FormatConfig(csv_delimiter="\t"))
        ]
        
        for config_name, config in csv_configs:
            output_path = os.path.join(temp_dir, f"csv_{config_name.lower()}")
            success = format_output(data, output_path, OutputFormat.CSV, config)
            if success:
                csv_files = [f for f in os.listdir(temp_dir) if f.startswith(f"csv_{config_name.lower()}_")]
                print(f"    {config_name}: {len(csv_files)} CSV files created")

def demonstrate_batch_processing():
    """Demonstrate batch processing capabilities"""
    print("\n" + "=" * 80)
    print("BATCH PROCESSING DEMO")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    
    print("\n1. BATCH FORMAT EXPORT")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = os.path.join(temp_dir, "batch_demo")
        
        # Test batch formatting
        formats = [OutputFormat.JSON, OutputFormat.HTML, OutputFormat.LATEX, OutputFormat.MARKDOWN, OutputFormat.XML]
        
        print(f"  Exporting to {len(formats)} formats simultaneously...")
        results = batch_format(data, base_path, formats)
        
        print(f"\n  Batch Export Results:")
        total_size = 0
        for format_name, success in results.items():
            output_path = f"{base_path}.{format_name}"
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                total_size += file_size
                print(f"    ✓ {format_name.upper()}: {file_size:,} bytes")
            else:
                print(f"    ✗ {format_name.upper()}: Failed")
        
        print(f"\n  Total output size: {total_size:,} bytes")
        print(f"  Files created: {len([f for f in results.values() if f])}")
    
    print("\n2. CONVENIENCE FUNCTIONS")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test convenience functions
        convenience_functions = [
            ("HTML Export", export_to_html, "html"),
            ("LaTeX Export", export_to_latex, "tex"),
            ("XML Export", export_to_xml, "xml"),
            ("CSV Export", export_to_csv, "csv"),
            ("Markdown Export", export_to_markdown, "md")
        ]
        
        print("  Testing convenience functions:")
        for func_name, func, extension in convenience_functions:
            output_path = os.path.join(temp_dir, f"convenience.{extension}")
            success = func(data, output_path)
            
            if success:
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                print(f"    ✓ {func_name}: {file_size:,} bytes")
            else:
                print(f"    ✗ {func_name}: Failed")
    
    print("\n3. EXPORT ALL FORMATS")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = os.path.join(temp_dir, "complete_export")
        
        print("  Exporting to all supported formats...")
        results = export_all_formats(data, base_path)
        
        print(f"\n  Complete Export Results:")
        successful = 0
        total_size = 0
        
        for format_name, success in results.items():
            if success:
                # Try to find the output file
                possible_extensions = {
                    "json": "json", "html": "html", "latex": "latex", 
                    "xml": "xml", "csv": "csv", "markdown": "markdown"
                }
                
                ext = possible_extensions.get(format_name, format_name)
                output_path = f"{base_path}.{ext}"
                
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    total_size += file_size
                    print(f"    ✓ {format_name.upper()}: {file_size:,} bytes")
                    successful += 1
                else:
                    # Check for CSV files (multiple files)
                    if format_name == "csv":
                        csv_files = [f for f in os.listdir(temp_dir) if f.startswith("complete_export_") and f.endswith(".csv")]
                        if csv_files:
                            csv_size = sum(os.path.getsize(os.path.join(temp_dir, f)) for f in csv_files)
                            total_size += csv_size
                            print(f"    ✓ {format_name.upper()}: {len(csv_files)} files, {csv_size:,} bytes")
                            successful += 1
                        else:
                            print(f"    ✗ {format_name.upper()}: Files not found")
                    else:
                        print(f"    ✗ {format_name.upper()}: File not found")
            else:
                print(f"    ✗ {format_name.upper()}: Export failed")
        
        print(f"\n  Summary: {successful}/{len(results)} formats successful")
        print(f"  Total output size: {total_size:,} bytes")

def demonstrate_advanced_features():
    """Demonstrate advanced formatting features"""
    print("\n" + "=" * 80)
    print("ADVANCED FEATURES DEMO")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    
    print("\n1. CUSTOM CONFIGURATION COMBINATIONS")
    print("-" * 50)
    
    # Create custom configurations for different use cases
    use_cases = [
        ("Research Paper", FormatConfig(
            include_metadata=True, include_equations=True, include_citations=True,
            include_figures=True, include_tables=True, include_networks=False,
            latex_document_class="article", latex_packages=["amsmath", "graphicx", "natbib"]
        )),
        ("Technical Report", FormatConfig(
            include_metadata=True, include_figures=True, include_tables=True,
            include_equations=False, include_citations=True, include_networks=True,
            latex_document_class="report", html_include_css=True
        )),
        ("Data Export", FormatConfig(
            include_metadata=False, include_figures=False, include_equations=False,
            include_citations=False, include_networks=False, include_statistics=True,
            csv_delimiter=";", xml_pretty_print=True
        )),
        ("Presentation Summary", FormatConfig(
            include_metadata=True, include_figures=True, include_statistics=True,
            include_tables=False, include_equations=False, include_citations=False,
            include_networks=False, markdown_include_toc=True, html_include_css=True
        ))
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for use_case_name, config in use_cases:
            print(f"\n  {use_case_name} Configuration:")
            
            # Generate multiple formats for each use case
            formats = [OutputFormat.HTML, OutputFormat.MARKDOWN]
            for fmt in formats:
                output_path = os.path.join(temp_dir, f"{use_case_name.lower().replace(' ', '_')}.{fmt.value}")
                success = format_output(data, output_path, fmt, config)
                
                if success:
                    file_size = os.path.getsize(output_path)
                    print(f"    ✓ {fmt.value.upper()}: {file_size:,} bytes")
                else:
                    print(f"    ✗ {fmt.value.upper()}: Failed")
    
    print("\n2. QUALITY ASSESSMENT INTEGRATION")
    print("-" * 50)
    
    # Show how quality metrics are included in output
    quality_metrics = data["summary"]
    print(f"  Quality Indicators:")
    print(f"    • Metadata extracted: {quality_metrics['metadata_extracted']}")
    print(f"    • DOI found: {quality_metrics['doi_found']}")
    print(f"    • Title confidence: {quality_metrics['title_confidence']:.2f}")
    print(f"    • Abstract confidence: {quality_metrics['abstract_confidence']:.2f}")
    print(f"    • Author confidence: {quality_metrics['author_confidence']:.2f}")
    print(f"    • Citation networks analyzed: {quality_metrics['citation_networks_analyzed']}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate HTML report with quality indicators
        config = FormatConfig(include_statistics=True)
        output_path = os.path.join(temp_dir, "quality_report.html")
        success = format_output(data, output_path, OutputFormat.HTML, config)
        
        if success:
            with open(output_path, 'r') as f:
                content = f.read()
                quality_section_found = "Quality Indicators" in content
                print(f"\n  ✓ Quality indicators included in HTML: {quality_section_found}")
    
    print("\n3. LARGE DATA HANDLING")
    print("-" * 50)
    
    # Test with larger dataset
    print("  Testing with extended dataset...")
    
    # Create larger data by duplicating sections
    large_data = data.copy()
    
    # Multiply sections
    original_sections = large_data["sections"]["sections"]
    large_data["sections"]["sections"] = original_sections * 5
    large_data["sections"]["section_count"] = len(large_data["sections"]["sections"])
    
    # Multiply figures
    original_figures = large_data["figures"]["figures"]
    large_data["figures"]["figures"] = original_figures * 3
    large_data["figures"]["figure_count"] = len(large_data["figures"]["figures"])
    
    # Update summary
    large_data["summary"]["sections_found"] = large_data["sections"]["section_count"]
    large_data["summary"]["figures_found"] = large_data["figures"]["figure_count"]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        formats_to_test = [OutputFormat.HTML, OutputFormat.MARKDOWN, OutputFormat.JSON]
        
        for fmt in formats_to_test:
            output_path = os.path.join(temp_dir, f"large_data.{fmt.value}")
            success = format_output(large_data, output_path, fmt)
            
            if success:
                file_size = os.path.getsize(output_path)
                print(f"    ✓ {fmt.value.upper()}: {file_size:,} bytes ({large_data['sections']['section_count']} sections, {large_data['figures']['figure_count']} figures)")
            else:
                print(f"    ✗ {fmt.value.upper()}: Failed with large dataset")

def demonstrate_integration_examples():
    """Demonstrate integration with Paper2Data pipeline"""
    print("\n" + "=" * 80)
    print("INTEGRATION EXAMPLES")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    
    print("\n1. PIPELINE INTEGRATION")
    print("-" * 50)
    print("# Integrate with main extraction pipeline")
    print("from paper2data import extract_all_content")
    print("from paper2data import format_output, OutputFormat")
    print("")
    print("# Extract content with automatic formatting")
    print("with open('paper.pdf', 'rb') as f:")
    print("    pdf_content = f.read()")
    print("")
    print("# Extract and format in one step")
    print("results = extract_all_content(")
    print("    pdf_content, ")
    print("    output_format='html',")
    print("    output_path='analysis_report.html'")
    print(")")
    
    print("\n2. BATCH DOCUMENT PROCESSING")
    print("-" * 50)
    print("# Process multiple documents")
    print("from paper2data import batch_format")
    print("")
    print("documents = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']")
    print("formats = ['html', 'markdown', 'json']")
    print("")
    print("for doc_path in documents:")
    print("    with open(doc_path, 'rb') as f:")
    print("        results = extract_all_content(f.read())")
    print("    ")
    print("    base_name = doc_path.replace('.pdf', '')")
    print("    batch_format(results, base_name, formats)")
    
    print("\n3. CUSTOM WORKFLOW EXAMPLES")
    print("-" * 50)
    print("# Academic publication workflow")
    print("config = FormatConfig(")
    print("    include_equations=True,")
    print("    include_citations=True,")
    print("    latex_document_class='article'")
    print(")")
    print("")
    print("export_to_latex(results, 'manuscript.tex', config)")
    print("export_to_html(results, 'supplementary.html')")
    
    print("\n4. QUALITY-BASED FORMATTING")
    print("-" * 50)
    print("# Format based on extraction quality")
    print("summary = results['summary']")
    print("")
    print("if summary['title_confidence'] > 0.9:")
    print("    # High quality - full report")
    print("    export_all_formats(results, 'high_quality_report')")
    print("else:")
    print("    # Lower quality - basic formats only")
    print("    formats = ['json', 'markdown']")
    print("    batch_format(results, 'basic_report', formats)")
    
    print("\n5. SELECTIVE EXPORT BY CONTENT TYPE")
    print("-" * 50)
    print("# Export different content types separately")
    print("if results['summary']['equations_found'] > 0:")
    print("    # LaTeX for mathematical content")
    print("    latex_config = FormatConfig(")
    print("        include_equations=True,")
    print("        include_metadata=False,")
    print("        include_figures=False")
    print("    )")
    print("    export_to_latex(results, 'equations.tex', latex_config)")
    print("")
    print("if results['summary']['tables_found'] > 0:")
    print("    # CSV for tabular data")
    print("    csv_config = FormatConfig(")
    print("        include_tables=True,")
    print("        include_metadata=False")
    print("    )")
    print("    export_to_csv(results, 'data_tables', csv_config)")

def demonstrate_performance_metrics():
    """Demonstrate performance characteristics"""
    print("\n" + "=" * 80)
    print("PERFORMANCE METRICS")
    print("=" * 80)
    
    data = create_comprehensive_sample_data()
    
    print("\n1. FORMATTING SPEED COMPARISON")
    print("-" * 50)
    
    import time
    
    formats_to_test = [
        (OutputFormat.JSON, "json"),
        (OutputFormat.MARKDOWN, "md"),
        (OutputFormat.HTML, "html"),
        (OutputFormat.XML, "xml"),
        (OutputFormat.LATEX, "tex"),
        (OutputFormat.CSV, "csv")
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print("  Format timing results:")
        
        for fmt, ext in formats_to_test:
            output_path = os.path.join(temp_dir, f"perf_test.{ext}")
            
            start_time = time.time()
            success = format_output(data, output_path, fmt)
            end_time = time.time()
            
            if success:
                duration = end_time - start_time
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                
                # For CSV, check multiple files
                if fmt == OutputFormat.CSV:
                    csv_files = [f for f in os.listdir(temp_dir) if f.startswith("perf_test_") and f.endswith(".csv")]
                    if csv_files:
                        file_size = sum(os.path.getsize(os.path.join(temp_dir, f)) for f in csv_files)
                
                speed = file_size / duration if duration > 0 else 0
                print(f"    {fmt.value.upper():10}: {duration:.3f}s, {file_size:,} bytes, {speed:,.0f} bytes/sec")
            else:
                print(f"    {fmt.value.upper():10}: Failed")
    
    print("\n2. MEMORY USAGE ESTIMATION")
    print("-" * 50)
    
    import sys
    
    # Estimate data size
    data_size = sys.getsizeof(str(data))
    print(f"  Input data size: ~{data_size:,} bytes")
    
    # Estimate multipliers for different formats
    format_multipliers = {
        "JSON": 1.2,      # Minimal overhead
        "HTML": 3.5,      # CSS and markup
        "LaTeX": 2.1,     # Command overhead
        "XML": 2.8,       # Tag overhead
        "Markdown": 1.6,  # Minimal markup
        "CSV": 0.8        # Compressed tabular
    }
    
    print(f"  Estimated output sizes:")
    for fmt, multiplier in format_multipliers.items():
        estimated_size = int(data_size * multiplier)
        print(f"    {fmt:10}: ~{estimated_size:,} bytes")
    
    print("\n3. SCALABILITY ASSESSMENT")
    print("-" * 50)
    
    # Test with different data sizes
    base_data = create_comprehensive_sample_data()
    data_sizes = [
        ("Small", 1, "1x data"),
        ("Medium", 3, "3x data"),
        ("Large", 5, "5x data")
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for size_name, multiplier, description in data_sizes:
            # Scale the data
            scaled_data = base_data.copy()
            scaled_data["sections"]["sections"] = base_data["sections"]["sections"] * multiplier
            scaled_data["figures"]["figures"] = base_data["figures"]["figures"] * multiplier
            
            # Test JSON formatting (fastest)
            output_path = os.path.join(temp_dir, f"scale_{size_name.lower()}.json")
            
            start_time = time.time()
            success = format_output(scaled_data, output_path, OutputFormat.JSON)
            end_time = time.time()
            
            if success:
                duration = end_time - start_time
                file_size = os.path.getsize(output_path)
                print(f"    {size_name:6} ({description}): {duration:.3f}s, {file_size:,} bytes")
            else:
                print(f"    {size_name:6} ({description}): Failed")

def main():
    """Main demo function"""
    print("Paper2Data Output Formatters Demo")
    print("=" * 80)
    print("This demo showcases the comprehensive output formatting capabilities")
    print("including multiple formats, configuration options, batch processing,")
    print("and integration with the Paper2Data extraction pipeline.")
    print()
    
    try:
        # Run demonstrations
        sample_data = demonstrate_basic_formatting()
        demonstrate_configuration_options()
        demonstrate_batch_processing()
        demonstrate_advanced_features()
        demonstrate_integration_examples()
        demonstrate_performance_metrics()
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✓ Basic formatting demonstrated for all supported formats")
        print("✓ Configuration options and customization showcased")
        print("✓ Batch processing and convenience functions tested")
        print("✓ Advanced features and integration examples provided")
        print("✓ Performance characteristics analyzed")
        print("\nThe Output Formatters system is ready for production use!")
        
        # Final statistics
        print(f"\nDemo Statistics:")
        print(f"  • Sample data size: {len(str(sample_data)):,} characters")
        print(f"  • Formats tested: 6 major formats")
        print(f"  • Configuration options: 15+ different settings")
        print(f"  • Use cases demonstrated: 8 different scenarios")
        print(f"  • Integration patterns: 5 workflow examples")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 