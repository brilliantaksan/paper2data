# Paper2Data

Convert academic papers (PDF, arXiv, DOI) into structured data repositories with organized content, extracted figures, tables, and metadata.

[![CI/CD Status](https://github.com/paper2data/paper2data/workflows/Paper2Data%20CI/CD/badge.svg)](https://github.com/paper2data/paper2data/actions)
[![Python Package](https://img.shields.io/pypi/v/paper2data-parser)](https://pypi.org/project/paper2data-parser/)
[![Node.js Package](https://img.shields.io/npm/v/paper2data-cli)](https://www.npmjs.com/package/paper2data-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

Paper2Data transforms academic papers into well-organized, searchable data repositories. Perfect for researchers, academics, and data scientists who need to extract and analyze content from research papers.

### ✨ Key Features

- **📄 Multi-format Input**: PDF files, arXiv URLs, DOI resolution
- **🔍 Intelligent Parsing**: Extract sections, figures, tables, and citations
- **📁 Repository Generation**: Create organized Git repositories with structured content
- **🎨 Multiple Output Formats**: Markdown, CSV, JSON, HTML
- **🔧 CLI Interface**: User-friendly command-line tool
- **🐍 Python API**: Programmatic access for automation
- **🔌 Extensible**: Plugin system for custom processing

## 🚀 Quick Start

### Installation

```bash
# Install CLI tool (includes Python parser)
npm install -g paper2data-cli

# Or install Python package directly
pip install paper2data-parser
```

### Basic Usage

```bash
# Convert a PDF file
paper2data convert paper.pdf

# Convert from arXiv
paper2data convert https://arxiv.org/abs/2103.15522

# Convert from DOI
paper2data convert 10.1038/nature12373

# Batch process multiple papers
paper2data convert batch ./papers/ --output ./processed/
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

**🚧 Currently in Development**

Paper2Data is actively being developed. The project structure and interfaces are ready, with core functionality being implemented in stages:

### ✅ Completed
- [x] Project structure and monorepo setup
- [x] CLI interface design and command structure
- [x] Python package architecture
- [x] CI/CD pipeline configuration
- [x] Comprehensive documentation

### 🔄 In Progress (Stage 1)
- [ ] Python development environment setup
- [ ] Basic PDF text extraction
- [ ] CLI-Python integration
- [ ] Error handling framework
- [ ] Unit testing infrastructure

### 📋 Planned (Stages 2-4)
- [ ] Advanced content extraction (figures, tables)
- [ ] arXiv and DOI integration
- [ ] Repository generation system
- [ ] Plugin architecture
- [ ] Performance optimization

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

# Setup Python environment
cd packages/parser
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"

# Setup Node.js environment  
cd ../cli
npm install
npm link  # Makes paper2data command available globally

# Run tests
cd ../../
python -m pytest packages/parser/tests/
npm test --prefix packages/cli
python tests/integration_test.py
```

### Testing the Setup

```bash
# Test CLI interface
paper2data --help
paper2data convert --help

# Test Python parser
cd packages/parser
pytest -v

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
  - PDFPlumber for table detection
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

### Version 1.0 (Current Development)
- Core PDF parsing and content extraction
- CLI interface with basic commands
- Repository generation with standard templates
- arXiv and DOI integration

### Version 1.1 (Future)
- Advanced figure and table extraction
- Plugin architecture for custom processors
- Multiple output format templates
- Batch processing optimization

### Version 2.0 (Future)
- Web interface for non-technical users
- Cloud processing capabilities
- Advanced citation analysis
- Integration with reference managers

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