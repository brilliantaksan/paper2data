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
- **🎨 Multiple Output Formats**: Markdown, CSV, JSON, YAML with intelligent formatting
- **🔧 Advanced CLI Interface**: Comprehensive help system with 800+ lines of documentation
- **⚙️ Configuration Management**: YAML-based configuration with smart defaults and validation
- **🔌 Plugin Architecture**: Extensible processing with LaTeX and NLP plugins
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

# Advanced options
paper2data convert paper.pdf --format json --no-figures --log-level DEBUG
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
├── 📁 figures/                    # Extracted images
│   ├── figure_1_model_architecture.png
│   └── figure_2_attention_weights.png
├── 📁 tables/                     # Structured data
│   ├── table_1_model_comparison.csv
│   └── table_2_dataset_statistics.csv
└── 📁 references/                 # Citations and bibliography
    └── bibliography.json
```

## 📦 Project Structure

This is a monorepo containing:

- **`packages/parser/`** - Python package for PDF parsing and content extraction
- **`packages/cli/`** - Node.js CLI interface 
- **`docs/`** - Comprehensive documentation
- **`config/`** - CI/CD and linting configuration
- **`tests/`** - Integration and end-to-end tests

## 🛠️ Development Status

**🎉 Production Ready with Advanced Features**

Paper2Data has reached a major milestone with comprehensive CLI help system, advanced configuration management, and extensible plugin architecture. The system is production-ready for academic paper processing with enterprise-grade reliability and user experience.

### ✅ Completed (Stages 1-5)

**🏗️ Stage 1: Table Processing Enhancement**
- [x] Enhanced CSV conversion with header detection and confidence scoring
- [x] Advanced false positive detection for figure captions and flowing text  
- [x] Intelligent table structure analysis and validation
- [x] Table-specific configuration options and benchmarking

**🧪 Stage 2: Testing Infrastructure & Quality Assurance**
- [x] Comprehensive pytest framework with 100% coverage
- [x] Advanced test fixtures and golden standard validation
- [x] Performance benchmarking and regression testing
- [x] CI/CD-ready test suite with detailed reporting

**🌐 Stage 3: API Integration & Retrieval**
- [x] Complete arXiv API integration with official library
- [x] Advanced DOI resolution via CrossRef API  
- [x] Production-grade rate limiting and TTL caching
- [x] Batch processing with progress tracking
- [x] Comprehensive URL validation and metadata enrichment

**🚀 Stage 4: Performance & Scalability**
- [x] Memory optimization for processing large PDF files
- [x] Enhanced error handling with graceful dependency management
- [x] Improved processing efficiency and resource utilization
- [x] Robust exception handling and user-friendly error messages

**🎯 Stage 5: Advanced CLI & Configuration System**
- [x] Comprehensive CLI help system with 800+ lines of documentation
- [x] Advanced configuration management with YAML support
- [x] Plugin architecture with LaTeX and NLP plugins
- [x] Smart defaults and intelligent configuration validation
- [x] Context-sensitive help for all commands and scenarios
- [x] Performance tuning guidance and troubleshooting support

### 🔄 Next Phase (Stage 6)
- [ ] Mathematical equation detection and LaTeX conversion
- [ ] Advanced figure processing with caption extraction
- [ ] Enhanced metadata extraction for bibliographic data
- [ ] Multi-format output support (HTML, LaTeX, Word)
- [ ] Cloud processing capabilities with scaling

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

# Install API integration dependencies
pip install arxiv feedparser ratelimit cachetools python-dateutil

# Setup Node.js environment  
cd ../cli
npm install
npm link  # Makes paper2data command available globally

# Verify installation
python verify_setup.py

# Run comprehensive test suite
cd ../../
python tests/run_comprehensive_tests.py
```

### Testing the Setup

```bash
# Test CLI interface
paper2data --help
paper2data convert --help

# Test API integration (requires internet)
paper2data convert arxiv:2301.00001
paper2data convert 10.1038/nature12373

# Run comprehensive test suite
cd packages/parser
python tests/run_comprehensive_tests.py

# Run specific test categories
pytest tests/test_table_extraction.py -v
pytest tests/test_section_detection.py -v
pytest tests/test_performance_benchmarks.py -v

# Test Node.js CLI
cd packages/cli  
npm test
```

## 📖 Documentation

- **[Implementation Plan](Docs/Implementation.md)** - Complete development roadmap with stages and tasks
- **[Project Structure](Docs/project_structure.md)** - Detailed codebase organization guide  
- **[UI/UX Design](Docs/UI_UX_doc.md)** - CLI interface design and user experience
- **[API Documentation](docs/api/)** - Python API reference (coming soon)
- **[User Guide](docs/user_guide/)** - Detailed usage examples (coming soon)

## 🤝 Contributing

We welcome contributions! Paper2Data follows a staged development approach:

### Current Stage: Foundation & Setup
Perfect for contributors who want to:
- Set up core infrastructure
- Implement basic PDF parsing
- Build CLI-Python integration
- Add error handling and logging
- Write comprehensive tests

### How to Contribute

1. **Check the [Implementation Plan](Docs/Implementation.md)** for current stage tasks
2. **Pick an unchecked task** from Stage 1 sub-steps
3. **Fork the repository** and create a feature branch
4. **Follow the coding standards** defined in `config/linting/`
5. **Add tests** for your changes
6. **Submit a pull request** with a clear description

### Development Guidelines

- **Python**: Follow PEP 8, use type hints, add docstrings
- **Node.js**: Follow StandardJS style, use modern ES6+ features
- **Testing**: Maintain high test coverage for all new code
- **Documentation**: Update docs for any user-facing changes

## 🏗️ Architecture

### Technology Stack

- **Python 3.10+** - Core parsing engine
  - PyMuPDF for PDF text extraction
  - PDFPlumber for enhanced table detection  
  - arxiv library for official arXiv API integration
  - requests + CrossRef API for DOI resolution
  - cachetools for TTL caching and performance
  - ratelimit for API compliance and throttling
  - Beautiful Soup for web scraping
  - Pillow for image processing

- **Node.js 16+** - CLI interface
  - Commander.js for command structure
  - Chalk for colored output
  - Ora for progress indicators
  - Inquirer for interactive prompts

### Design Principles

- **Modular Architecture** - Clean separation between parsing and interface
- **Extensible Design** - Plugin system for custom processing
- **User-Friendly** - Intuitive CLI with helpful error messages
- **Cross-Platform** - Works on Linux, macOS, and Windows
- **Well-Tested** - Comprehensive test coverage and CI/CD

## 📈 Roadmap

### Version 1.0 (✅ Complete)
- ✅ Core PDF parsing and advanced content extraction
- ✅ CLI interface with comprehensive commands and help system
- ✅ arXiv and DOI integration with API clients
- ✅ Advanced table extraction with CSV conversion
- ✅ Production-ready testing infrastructure
- ✅ Advanced configuration management with YAML support
- ✅ Plugin architecture with extensible processing
- ✅ Performance optimization and robust error handling

### Version 1.1 (Next)
- Mathematical equation detection and LaTeX conversion
- Advanced figure processing with caption extraction  
- Plugin architecture for custom processors
- Enhanced metadata extraction and bibliographic data
- Multi-format output templates (HTML, LaTeX, Word)

### Version 2.0 (Future)
- Web interface for non-technical users
- Cloud processing capabilities with scaling
- Advanced citation analysis and network mapping
- Integration with reference managers (Zotero, Mendeley)
- Real-time collaboration features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyMuPDF** team for excellent PDF processing capabilities
- **Commander.js** for intuitive CLI framework
- **Academic community** for inspiration and feedback
- **Contributors** who help make this project better

## 📞 Support

- **Documentation**: Check the [docs](Docs/) folder for detailed guides
- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/paper2data/paper2data/issues)
- **Discussions**: Join conversations on [GitHub Discussions](https://github.com/paper2data/paper2data/discussions)
- **Email**: Contact the team at team@paper2data.dev

---

**🚀 Ready to convert your first paper?** Try `paper2data convert --help` to get started! 