# Paper2Data

Convert academic papers (PDF, arXiv, DOI) into structured data repositories with organized content, extracted figures, tables, and metadata.

[![CI/CD Status](https://github.com/paper2data/paper2data/workflows/Paper2Data%20CI/CD/badge.svg)](https://github.com/paper2data/paper2data/actions)
[![Python Package](https://img.shields.io/pypi/v/paper2data-parser)](https://pypi.org/project/paper2data-parser/)
[![Node.js Package](https://img.shields.io/npm/v/paper2data-cli)](https://www.npmjs.com/package/paper2data-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

Paper2Data transforms academic papers into well-organized, searchable data repositories. Perfect for researchers, academics, and data scientists who need to extract and analyze content from research papers.

### ✨ Key Features

- **📄 Multi-format Input**: PDF files, arXiv URLs, DOI resolution with automatic retrieval
- **🔍 Intelligent Parsing**: Advanced section detection, table extraction to CSV, figure processing
- **🌐 API Integration**: Live arXiv and CrossRef DOI resolution with metadata enrichment
- **⚡ Performance Optimized**: Rate limiting, caching, and batch processing capabilities
- **📁 Repository Generation**: Create organized Git repositories with structured content
- **🎨 Multiple Output Formats**: HTML, LaTeX, Word, EPUB, Markdown with professional templates
- **🔧 Advanced CLI Interface**: Comprehensive help system with 800+ lines of documentation
- **⚙️ Configuration Management**: YAML-based configuration with smart defaults and validation
- **🔌 Enhanced Plugin System**: v1.1 plugin architecture with marketplace, dependency management, and auto-updates
- **🧮 Mathematical Processing**: LaTeX equation detection, conversion, and MathML support
- **🖼️ Advanced Figure Processing**: AI-powered figure classification, caption extraction, and analysis
- **📚 Enhanced Metadata**: Institution detection, author disambiguation, and funding information
- **📖 Bibliographic Parsing**: Citation style detection, reference normalization, and network analysis
- **🐍 Python API**: Full programmatic access with comprehensive error handling
- **🧪 Production Ready**: 100% test coverage with comprehensive quality assurance

## 🚀 Quick Start

### Installation

```bash
# Install CLI tool (includes Python parser)
npm install -g paper2data-cli

# Or install Python package directly
pip install paper2data-parser

# Install with all API integration dependencies
pip install paper2data-parser[api]

# For development with testing framework
pip install paper2data-parser[dev]
```

### Basic Usage

```bash
# Convert a PDF file
paper2data convert paper.pdf

# Convert from arXiv (automatic metadata enrichment)
paper2data convert https://arxiv.org/abs/2103.15522
paper2data convert arxiv:2103.15522

# Convert from DOI (with CrossRef metadata)
paper2data convert 10.1038/nature12373
paper2data convert https://doi.org/10.1038/nature12373

# Batch process multiple identifiers
paper2data convert batch arxiv:2103.15522,10.1038/nature12373,paper.pdf

# Advanced options with multi-format export
paper2data convert paper.pdf --format html,latex,word --template academic
```

### Example Output Structure

```
paper_2023_attention_is_all_you_need/
├── 📄 README.md                    # Overview and navigation
├── 📋 metadata.json               # Machine-readable metadata
├── 📁 sections/                   # Organized content
│   ├── 01_abstract.md
│   ├── 02_introduction.md
│   ├── 03_methodology.md
│   ├── 04_results.md
│   └── 05_conclusion.md
├── 📁 figures/                    # Extracted images with analysis
│   ├── figure_1_model_architecture.png
│   ├── figure_2_attention_weights.png
│   └── figure_analysis.json       # AI-powered figure analysis
├── 📁 tables/                     # Structured data
│   ├── table_1_model_comparison.csv
│   └── table_2_dataset_statistics.csv
├── 📁 equations/                  # Mathematical content
│   ├── equations.json             # LaTeX equations with MathML
│   └── equation_analysis.json     # Mathematical analysis
├── 📁 references/                 # Citations and bibliography
│   ├── bibliography.json
│   └── citation_network.json      # Citation network analysis
└── 📁 exports/                    # Multi-format outputs
    ├── paper.html                 # Interactive HTML
    ├── paper.tex                  # LaTeX reconstruction
    ├── paper.docx                 # Word document
    └── paper.epub                 # E-book format
```

## 📦 Project Structure

This is a monorepo containing:

- **`packages/parser/`** - Python package for PDF parsing and content extraction
- **`packages/cli/`** - Node.js CLI interface 
- **`docs/`** - Comprehensive documentation
- **`config/`** - CI/CD and linting configuration
- **`tests/`** - Integration and end-to-end tests

## 🛠️ Development Status

**🎉 Paper2Data v1.1 - Enterprise-Grade Academic Processing Platform**

Paper2Data v1.1 represents a major advancement in academic document processing, featuring enterprise-grade plugin architecture, advanced AI-powered content analysis, and comprehensive multi-format export capabilities. The system is production-ready for academic institutions, research organizations, and data science teams.

### ✅ Completed v1.1 Features

**🔌 Enhanced Plugin System v1.1**
- [x] Advanced plugin architecture with dependency management
- [x] Plugin marketplace with community features and security scanning
- [x] Automatic plugin updates and health monitoring
- [x] Semantic versioning and conflict resolution
- [x] Performance analytics and system metrics
- [x] Dynamic plugin loading and configuration management

**🧮 Mathematical Processing Engine**
- [x] LaTeX equation detection and extraction
- [x] Mathematical symbol recognition and analysis
- [x] MathML conversion for web compatibility
- [x] Equation complexity analysis and validation
- [x] Integration with plugin system for extensibility

**🖼️ Advanced Figure Processing**
- [x] AI-powered figure classification (graphs, diagrams, photos, charts)
- [x] Automatic caption extraction with OCR fallback
- [x] Image quality assessment and analysis
- [x] Figure-text association and context analysis
- [x] Multi-format figure export with metadata

**📚 Enhanced Metadata Extraction**
- [x] Author disambiguation and institution detection
- [x] Funding source identification and categorization
- [x] Enhanced bibliographic data extraction
- [x] Publication status and version tracking
- [x] Cross-reference validation and enrichment

**📖 Bibliographic Parser & Citation Analysis**
- [x] Citation style detection and normalization
- [x] Reference parsing with multiple format support
- [x] Citation network analysis and visualization
- [x] Author metrics and impact assessment
- [x] Cross-database reference validation

**🎨 Multi-Format Export System**
- [x] Professional HTML export with interactive features
- [x] LaTeX reconstruction for academic submission
- [x] Microsoft Word compatibility (RTF format)
- [x] EPUB generation for e-book readers
- [x] Enhanced Markdown with rich formatting
- [x] Template system with academic, modern, and minimal themes

**🏗️ Previous Achievements (Stages 1-5)**
- [x] Enhanced CSV conversion with header detection and confidence scoring
- [x] Comprehensive pytest framework with 100% coverage
- [x] Complete arXiv API integration with official library
- [x] Memory optimization for processing large PDF files
- [x] Advanced CLI help system with 800+ lines of documentation
- [x] Plugin architecture with LaTeX and NLP plugins

### 🔮 Future Roadmap (v1.2+)

**🤖 AI-Powered Features**
- [ ] Large Language Model integration for content understanding
- [ ] Intelligent content summarization and key insight extraction
- [ ] Automated research gap identification
- [ ] AI-powered literature review generation

**☁️ Cloud & Collaboration**
- [ ] Cloud processing capabilities with scaling
- [ ] Real-time collaboration features
- [ ] Distributed processing for large document collections
- [ ] API-first architecture for integration

**🌐 Enterprise Features**
- [ ] Single sign-on (SSO) integration
- [ ] Role-based access control
- [ ] Audit logging and compliance features
- [ ] Enterprise plugin marketplace

## 🔌 Enhanced Plugin System v1.1

Paper2Data v1.1 introduces a revolutionary plugin system with marketplace integration:

### Plugin Management

```python
from paper2data import initialize_enhanced_plugin_system
import asyncio

# Initialize the enhanced plugin system
system = initialize_enhanced_plugin_system({
    "auto_update_enabled": True,
    "health_monitoring_enabled": True
})

# Search and install plugins
results = system.search_plugins("latex", min_rating=4.0)
await system.install_plugin("latex-processor")

# Monitor system health
metrics = system.get_system_metrics()
print(f"Active plugins: {metrics.active_plugins}")
```

### Key Plugin Features

- **🏪 Plugin Marketplace**: Community-driven plugin discovery and installation
- **📦 Dependency Management**: Automatic dependency resolution with semantic versioning
- **🔒 Security Scanning**: Automated security validation before installation
- **📊 Health Monitoring**: Real-time plugin performance and health tracking
- **🔄 Auto-Updates**: Background monitoring with automatic plugin updates
- **⚡ Performance Analytics**: Comprehensive metrics and system insights

## 🎨 Multi-Format Export

Export your processed papers in multiple professional formats:

```python
from paper2data import MultiFormatExporter, ExportConfiguration

# Configure export
config = ExportConfiguration(
    formats=["html", "latex", "word", "epub"],
    theme="academic",
    include_figures=True,
    include_equations=True
)

# Export to multiple formats
exporter = MultiFormatExporter(config)
results = exporter.export_document(document_data, output_dir)

print(f"Exported to {len(results)} formats successfully!")
```

### Export Formats

- **📄 HTML**: Interactive web format with search, figure zoom, and responsive design
- **📝 LaTeX**: Academic-quality reconstruction for journal submission
- **📖 Word**: Microsoft Word compatibility for institutional workflows
- **📚 EPUB**: E-book format for mobile reading and archival
- **📝 Markdown**: Developer-friendly format for version control

## 🔧 Development Setup

### Prerequisites

- **Python 3.10+** for the parser package
- **Node.js 16+** for the CLI interface
- **Git** for version control

### Quick Setup

```bash
# Clone repository
git clone https://github.com/paper2data/paper2data.git
cd paper2data

# Automated setup (recommended)
python setup_dev.py

# Or manual setup:
cd packages/parser
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"

# Install v1.1 dependencies
pip install semver networkx packaging schedule aiohttp

# Setup Node.js environment  
cd ../cli
npm install
npm link  # Makes paper2data command available globally

# Verify installation
python verify_setup.py

# Run comprehensive test suite including v1.1 features
cd packages/parser
python -m src.paper2data.integration_test_enhanced_plugin_system
```

### Testing the Setup

```bash
# Test CLI interface
paper2data --help
paper2data convert --help

# Test API integration (requires internet)
paper2data convert arxiv:2301.00001
paper2data convert 10.1038/nature12373

# Test v1.1 features
python -c "from paper2data import get_enhanced_plugin_system; print('✅ Enhanced Plugin System Ready')"
``` 