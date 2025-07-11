# Paper2Data Project Structure

## Root Directory Structure

```bash
paper2data/
├── packages/
│   ├── parser/
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── ingest.py
│   │   │   ├── extractor.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   │   └── test_parser.py
│   │   └── pyproject.toml
│   ├── cli/
│   │   ├── src/
│   │   │   ├── index.js
│   │   │   ├── commands/
│   │   │   │   ├── init.js
│   │   │   │   └── convert.js
│   │   │   └── utils.js
│   │   ├── tests/
│   │   │   └── test_cli.js
│   │   └── package.json
│   └── examples/
│       ├── sample_paper.pdf
│       └── output_template/
├── docs/
│   ├── Implementation.md
│   ├── project_structure.md
│   └── UI_UX_doc.md
├── config/
│   ├── github-actions.yml
│   └── linting/
│       ├── eslint.json
│       └── flake8.ini
├── tests/
│   ├── integration_test.py
│   └── end_to_end.test.js
├── .gitignore
├── README.md
└── LICENSE
```

## Detailed Directory Structure

### `/packages/` - Monorepo Package Organization

The monorepo approach allows for independent development and deployment of Python and Node.js components while maintaining shared configuration and documentation.

#### `/packages/parser/` - Python Core Package
**Purpose:** PDF parsing, content extraction, and data processing

```
parser/
├── src/
│   ├── __init__.py              # Package initialization and main API
│   ├── ingest.py                # PDF/URL input handling and validation
│   ├── extractor.py             # Content extraction and processing logic
│   └── utils.py                 # Utility functions and helpers
├── tests/
│   └── test_parser.py           # Unit tests for parser functionality
└── pyproject.toml               # Python packaging and dependencies
```

**Key Modules:**

- **`ingest.py`** - Handles multiple input types:
  - PDF file validation and loading
  - arXiv URL processing and download
  - DOI resolution and paper retrieval
  - Input sanitization and error handling

- **`extractor.py`** - Core extraction functionality:
  - Text extraction using PyMuPDF
  - Section detection and parsing
  - Figure and table extraction
  - Metadata extraction and bibliography processing
  - Output formatting (Markdown, CSV, JSON)

- **`utils.py`** - Supporting utilities:
  - File system operations
  - Text processing and cleaning
  - Image processing and conversion
  - Progress tracking and logging
  - Configuration management

#### `/packages/cli/` - Node.js CLI Interface
**Purpose:** User-facing command-line interface and Python bridge

```
cli/
├── src/
│   ├── index.js                 # Main CLI entry point and argument parsing
│   ├── commands/
│   │   ├── init.js              # Repository initialization command
│   │   └── convert.js           # Main conversion command
│   └── utils.js                 # CLI utilities and Python bridge
├── tests/
│   └── test_cli.js              # CLI command and integration tests
└── package.json                 # Node.js dependencies and scripts
```

**Key Modules:**

- **`index.js`** - CLI framework setup:
  - Commander.js configuration
  - Global options and help system
  - Version management and updates
  - Error handling and user feedback

- **`commands/init.js`** - Repository setup:
  - Project initialization workflow
  - Configuration file generation
  - Template selection and customization
  - Git repository initialization

- **`commands/convert.js`** - Main conversion logic:
  - Input validation and preprocessing
  - Python subprocess management
  - Progress tracking and user feedback
  - Output validation and post-processing

- **`utils.js`** - CLI utilities:
  - Python environment detection
  - Process management and communication
  - Progress indicators and formatting
  - Configuration file handling

#### `/packages/examples/` - Sample Data and Templates
**Purpose:** Demonstration materials and output templates

```
examples/
├── sample_paper.pdf             # Example academic paper for testing
└── output_template/             # Standard output repository structure
    ├── README.md.template       # Repository README template
    ├── metadata.json.template   # Metadata structure template
    ├── sections/                # Section organization example
    ├── figures/                 # Figure output structure
    ├── tables/                  # Table output structure
    └── .gitignore.template      # Git ignore template for generated repos
```

### `/docs/` - Documentation
**Purpose:** Project documentation and specifications

```
docs/
├── Implementation.md            # Complete implementation plan with stages
├── project_structure.md         # This file - project organization guide
└── UI_UX_doc.md                # CLI design and user experience guide
```

### `/config/` - Configuration and CI/CD
**Purpose:** Build, deployment, and code quality configuration

```
config/
├── github-actions.yml           # CI/CD workflow definitions
└── linting/
    ├── eslint.json              # JavaScript/Node.js linting rules
    └── flake8.ini               # Python code style and linting rules
```

**Configuration Details:**

- **`github-actions.yml`** - Automated workflows:
  - Multi-platform testing (Linux, macOS, Windows)
  - Python and Node.js environment matrix testing
  - Package publishing to PyPI and npm
  - Documentation deployment
  - Security scanning and dependency updates

- **`linting/`** - Code quality enforcement:
  - ESLint configuration for consistent JavaScript style
  - Flake8 rules for Python PEP 8 compliance
  - Pre-commit hooks integration
  - IDE integration guidelines

### `/tests/` - Integration and End-to-End Testing
**Purpose:** Cross-package testing and complete workflow validation

```
tests/
├── integration_test.py          # Python-based integration tests
└── end_to_end.test.js          # Node.js end-to-end workflow tests
```

**Testing Strategy:**

- **`integration_test.py`** - Parser integration:
  - Multi-format PDF processing tests
  - arXiv/DOI integration validation
  - Output format verification
  - Error handling and edge cases

- **`end_to_end.test.js`** - Complete workflows:
  - CLI command testing with real inputs
  - Python-Node.js communication validation
  - Repository generation verification
  - User experience flow testing

## File Naming Conventions

### Python Files (`/packages/parser/`)
- **Modules:** `snake_case.py` (e.g., `ingest.py`, `extractor.py`)
- **Classes:** `PascalCase` (e.g., `PDFIngestor`, `ContentExtractor`)
- **Functions:** `snake_case` (e.g., `extract_figures`, `parse_citations`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DEFAULT_OUTPUT_DIR`, `MAX_FILE_SIZE`)

### JavaScript Files (`/packages/cli/`)
- **Files:** `camelCase.js` (e.g., `index.js`, `convert.js`)
- **Functions:** `camelCase` (e.g., `convertPaper`, `initializeRepo`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`, `PYTHON_COMMAND`)

### Configuration Files
- **Python:** `pyproject.toml` for package configuration
- **Node.js:** `package.json` for dependencies and scripts
- **Linting:** `eslint.json`, `flake8.ini` for code quality rules

### Output Structure (Generated Repositories)
- **Directories:** `kebab-case` (e.g., `extracted-figures`, `table-data`)
- **Files:** `snake_case` with descriptive names (e.g., `01_introduction.md`, `figure_1_architecture.png`)

## Module Dependencies and Communication

### Package Interaction Flow
```
CLI Package (Node.js)
    ↓ subprocess calls
Parser Package (Python)
    ↓ file system operations
Generated Repository Structure
```

### Dependency Management

#### Python Package (`pyproject.toml`)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "paper2data-parser"
version = "1.0.0"
dependencies = [
    "PyMuPDF>=1.23.0",
    "pdfplumber>=0.9.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "pyyaml>=6.0",
    "pillow>=10.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0"
]
```

#### Node.js Package (`package.json`)
```json
{
  "name": "paper2data-cli",
  "version": "1.0.0",
  "main": "src/index.js",
  "bin": {
    "paper2data": "src/index.js"
  },
  "dependencies": {
    "commander": "^11.0.0",
    "chalk": "^5.3.0",
    "ora": "^7.0.1",
    "inquirer": "^9.2.0"
  },
  "devDependencies": {
    "jest": "^29.6.0",
    "eslint": "^8.45.0"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
```

## Environment Configuration

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/your-org/paper2data.git
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
npm test tests/end_to_end.test.js
```

### Production Build Process
```bash
# Build Python package
cd packages/parser
python -m build

# Build Node.js package
cd ../cli
npm pack

# Run integration tests
cd ../../tests
python integration_test.py
npm test end_to_end.test.js
```

## Build & Deployment Structure

### CI/CD Pipeline (`config/github-actions.yml`)
```yaml
name: Paper2Data CI/CD

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
  test-nodejs:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ['16', '18', '20']
    
  integration-tests:
    needs: [test-python, test-nodejs]
    runs-on: ubuntu-latest
    
  publish:
    if: startsWith(github.ref, 'refs/tags/')
    needs: [integration-tests]
    runs-on: ubuntu-latest
```

### Package Publishing

#### Python Package (PyPI)
- **Package name:** `paper2data-parser`
- **Installation:** `pip install paper2data-parser`
- **Import:** `from paper2data import ingest, extractor`

#### Node.js Package (npm)
- **Package name:** `paper2data-cli`
- **Installation:** `npm install -g paper2data-cli`
- **Usage:** `paper2data convert paper.pdf`

## Monorepo Benefits

### Development Advantages
- **Shared configuration** across Python and Node.js components
- **Unified testing** and CI/CD pipelines
- **Consistent documentation** and issue tracking
- **Synchronized releases** between CLI and parser

### Deployment Flexibility
- **Independent publishing** to PyPI and npm
- **Version synchronization** between packages
- **Gradual rollout** of features across components
- **Language-specific optimization** while maintaining integration

This monorepo structure provides clear separation of concerns while enabling seamless integration between the Python processing engine and Node.js CLI interface, supporting both developer productivity and user experience. 