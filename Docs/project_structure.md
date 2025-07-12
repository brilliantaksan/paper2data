# Paper2Data - Project Structure Documentation

## 📁 **Current Project Structure**

```
Paper2Data/
├── config/                           # Configuration files
│   ├── github-actions.yml           # CI/CD workflow configuration
│   └── linting/                     # Code quality configuration
│       ├── eslint.json             # JavaScript linting rules
│       └── flake8.ini              # Python linting configuration
│
├── Docs/                            # Documentation directory
│   ├── Implementation.md            # Comprehensive implementation roadmap
│   ├── project_structure.md         # This file - project organization
│   └── UI_UX_doc.md                # User experience guidelines
│
├── examples/                        # Usage examples and tutorials
│   └── sample_pdfs/                # Sample PDF files for testing
│
├── packages/                        # Core packages directory
│   ├── cli/                        # Node.js CLI wrapper
│   │   ├── package.json            # CLI dependencies and scripts
│   │   ├── package-lock.json       # Locked dependency versions
│   │   ├── src/                    # CLI source code
│   │   │   ├── commands/          # CLI command implementations
│   │   │   │   ├── convert.js     # Main conversion command
│   │   │   │   └── init.js        # Project initialization
│   │   │   └── index.js           # CLI entry point
│   │   └── tests/                 # CLI unit tests
│   │       └── test_cli.js        # CLI functionality tests
│   │
│   └── parser/                      # Python core processing engine
│       ├── pyproject.toml          # Python project configuration
│       ├── src/                    # Python source code
│       │   └── paper2data/         # Main package
│       │       ├── __init__.py     # Package initialization
│       │       ├── __main__.py     # CLI entry point
│       │       ├── extractor.py    # Core extraction logic
│       │       ├── ingest.py       # Input handling and validation
│       │       ├── main.py         # Main processing orchestration
│       │       └── utils.py        # Utility functions and helpers
│       ├── tests/                  # Python unit tests
│       │   └── test_parser.py      # Parser functionality tests
│       └── venv/                   # Virtual environment (development)
│
├── paper2data/                      # Symbolic links for CLI access
│   ├── cli                         # Link to packages/cli
│   ├── create-package              # Package creation utilities
│   └── parser                      # Link to packages/parser
│
├── tests/                          # Integration and end-to-end tests
│   ├── end_to_end.test.js         # Full workflow testing
│   └── integration_test.py        # Python integration tests
│
├── README.md                       # Project overview and quick start
├── setup_dev.py                   # Development environment setup
└── verify_setup.py                # Installation verification
```

---

## 🎯 **Enhanced Structure Plan**

### **Stage 1: Table Processing Enhancement**

```
packages/parser/src/paper2data/
├── extractors/                     # Specialized extraction modules
│   ├── __init__.py
│   ├── base_extractor.py          # Base extraction interface
│   ├── table_extractor.py         # Enhanced table processing
│   ├── figure_extractor.py        # Figure extraction logic
│   ├── section_extractor.py       # Section detection
│   └── citation_extractor.py      # Citation processing
│
├── formats/                        # Output format handlers
│   ├── __init__.py
│   ├── csv_writer.py              # CSV table output
│   ├── markdown_writer.py         # Markdown formatting
│   ├── json_writer.py             # JSON metadata output
│   └── html_writer.py             # HTML export (future)
│
└── table_processing/               # Table-specific components
    ├── __init__.py
    ├── detection.py               # Table detection algorithms
    ├── structure_analysis.py      # Row/column identification
    ├── confidence_scoring.py      # Quality assessment
    └── csv_conversion.py          # CSV formatting logic
```

### **Stage 2: Testing Infrastructure**

```
tests/
├── unit/                           # Unit tests
│   ├── test_extractors/           # Extractor module tests
│   │   ├── test_table_extractor.py
│   │   ├── test_figure_extractor.py
│   │   └── test_section_extractor.py
│   ├── test_formats/              # Output format tests
│   │   ├── test_csv_writer.py
│   │   └── test_markdown_writer.py
│   └── test_utils/                # Utility function tests
│       └── test_helpers.py
│
├── integration/                    # Integration tests
│   ├── test_full_pipeline.py     # End-to-end workflow
│   ├── test_api_integration.py   # API functionality
│   └── test_batch_processing.py  # Performance testing
│
├── fixtures/                      # Test data and fixtures
│   ├── sample_pdfs/              # Test PDF documents
│   ├── expected_outputs/         # Golden standard results
│   └── mock_responses/           # API response mocks
│
├── benchmarks/                    # Performance benchmarks
│   ├── speed_tests.py            # Processing speed tests
│   ├── memory_tests.py           # Memory usage analysis
│   └── accuracy_tests.py         # Output quality metrics
│
└── conftest.py                    # pytest configuration
```

### **Stage 3: API Integration**

```
packages/parser/src/paper2data/
├── apis/                          # External API integrations
│   ├── __init__.py
│   ├── base_api.py               # Base API client interface
│   ├── arxiv_api.py              # arXiv integration
│   ├── crossref_api.py           # DOI resolution via CrossRef
│   ├── publisher_apis.py         # Publisher-specific APIs
│   └── rate_limiter.py           # API rate limiting
│
├── downloaders/                   # Paper download functionality
│   ├── __init__.py
│   ├── pdf_downloader.py         # PDF file retrieval
│   ├── url_validator.py          # URL parsing and validation
│   ├── cache_manager.py          # Download caching
│   └── batch_downloader.py       # Bulk download operations
│
└── metadata/                      # Metadata processing
    ├── __init__.py
    ├── extractor.py              # Metadata extraction
    ├── enricher.py               # External metadata enrichment
    ├── validator.py              # Metadata validation
    └── schema.py                 # Metadata schema definitions
```

### **Stage 4: Performance & Scalability**

```
packages/parser/src/paper2data/
├── processing/                    # Processing pipeline
│   ├── __init__.py
│   ├── pipeline.py               # Main processing pipeline
│   ├── batch_processor.py        # Batch processing logic
│   ├── parallel_processor.py     # Multiprocessing support
│   └── progress_tracker.py       # Progress monitoring
│
├── caching/                       # Caching system
│   ├── __init__.py
│   ├── file_cache.py            # File-based caching
│   ├── memory_cache.py          # In-memory caching
│   └── cache_config.py          # Cache configuration
│
└── monitoring/                    # Performance monitoring
    ├── __init__.py
    ├── metrics.py               # Performance metrics
    ├── profiler.py              # Code profiling
    └── resource_monitor.py      # System resource tracking
```

### **Stage 5: Advanced Features**

```
packages/parser/src/paper2data/
├── plugins/                       # Plugin architecture
│   ├── __init__.py
│   ├── plugin_manager.py         # Plugin loading and management
│   ├── hooks.py                  # Plugin hook definitions
│   └── examples/                 # Example plugins
│       ├── latex_plugin.py       # LaTeX equation processing
│       └── ocr_plugin.py         # OCR integration
│
├── equations/                     # Mathematical equation processing
│   ├── __init__.py
│   ├── detector.py               # Equation detection
│   ├── latex_converter.py        # LaTeX conversion
│   └── mathml_converter.py       # MathML support
│
└── advanced_processing/           # Advanced features
    ├── __init__.py
    ├── citation_network.py       # Citation analysis
    ├── semantic_analysis.py      # Content understanding
    └── quality_assessment.py     # Output quality scoring
```

---

## 📊 **Configuration Management**

### **Configuration File Structure**

```
config/
├── default.yaml                   # Default configuration settings
├── development.yaml               # Development environment config
├── production.yaml               # Production environment config
├── testing.yaml                  # Testing environment config
│
├── extractors/                    # Extractor-specific configs
│   ├── table_config.yaml         # Table extraction settings
│   ├── figure_config.yaml        # Figure extraction settings
│   └── section_config.yaml       # Section detection settings
│
├── apis/                         # API configuration
│   ├── arxiv_config.yaml        # arXiv API settings
│   ├── crossref_config.yaml     # CrossRef API settings
│   └── rate_limits.yaml         # Rate limiting configuration
│
└── output/                       # Output format configurations
    ├── csv_format.yaml          # CSV output settings
    ├── markdown_format.yaml     # Markdown formatting
    └── json_schema.yaml         # JSON output schema
```

### **Environment Variables**

```bash
# Core Configuration
PAPER2DATA_CONFIG_PATH=/path/to/config
PAPER2DATA_LOG_LEVEL=INFO
PAPER2DATA_CACHE_DIR=/tmp/paper2data_cache

# API Keys and Endpoints
ARXIV_API_KEY=your_api_key
CROSSREF_API_KEY=your_api_key
PUBLISHER_API_KEYS={"springer": "key1", "elsevier": "key2"}

# Performance Settings
PAPER2DATA_MAX_WORKERS=4
PAPER2DATA_MEMORY_LIMIT=2GB
PAPER2DATA_BATCH_SIZE=10

# Output Settings
PAPER2DATA_OUTPUT_DIR=./output
PAPER2DATA_TEMP_DIR=/tmp/paper2data_temp
```

---

## 🗂️ **Data Flow Architecture**

### **Input Processing Pipeline**

```
Input Sources → Validation → Processing → Enhancement → Output
     ↓              ↓           ↓           ↓           ↓
  PDF Files    URL/DOI      Extraction   Metadata    Structured
  arXiv URLs   Validation   Pipeline     Enrichment   Output
  DOI Links    File Check   Parallel     Citation     (CSV, MD,
  Local Files  Format Ver.  Processing   Analysis     JSON, etc.)
```

### **Module Dependencies**

```
main.py
├── ingest.py (Input handling)
│   ├── downloaders/ (API integration)
│   └── validators/ (Input validation)
├── extractor.py (Core processing)
│   ├── extractors/ (Specialized extraction)
│   ├── processing/ (Pipeline management)
│   └── caching/ (Performance optimization)
└── utils.py (Utilities and helpers)
    ├── formats/ (Output formatting)
    ├── monitoring/ (Performance tracking)
    └── plugins/ (Extensibility)
```

---

## 🔧 **Development Workflow**

### **File Naming Conventions**

| **Component** | **Pattern** | **Example** |
|--------------|-------------|-------------|
| Extractors | `{type}_extractor.py` | `table_extractor.py` |
| API Clients | `{service}_api.py` | `arxiv_api.py` |
| Output Formats | `{format}_writer.py` | `csv_writer.py` |
| Tests | `test_{module}.py` | `test_table_extractor.py` |
| Configuration | `{component}_config.yaml` | `table_config.yaml` |
| Plugins | `{name}_plugin.py` | `latex_plugin.py` |

### **Module Organization Principles**

1. **Single Responsibility**: Each module handles one specific aspect
2. **Clear Interfaces**: Well-defined APIs between modules
3. **Dependency Injection**: Configurable dependencies for testing
4. **Error Boundaries**: Isolated error handling per module
5. **Extensibility**: Plugin-friendly architecture

### **Import Structure**

```python
# Standard library imports
import os
import logging
from typing import Dict, List, Optional

# Third-party imports
import fitz
import pandas as pd
from pydantic import BaseModel

# Local imports
from paper2data.extractors.base_extractor import BaseExtractor
from paper2data.formats.csv_writer import CSVWriter
from paper2data.utils.helpers import clean_text
```

---

## 📦 **Package Distribution Structure**

### **PyPI Package Structure**

```
paper2data/
├── setup.py                      # Package setup configuration
├── pyproject.toml                # Modern Python packaging
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── MANIFEST.in                   # Package manifest
├── README.md                     # Package documentation
├── LICENSE                       # License information
└── paper2data/                   # Package source
    ├── __init__.py              # Package initialization
    ├── cli.py                   # Command-line interface
    └── [all source modules]     # Core functionality
```

### **Docker Container Structure**

```
docker/
├── Dockerfile                    # Container definition
├── docker-compose.yml           # Multi-service setup
├── requirements.docker.txt      # Container dependencies
└── entrypoint.sh                # Container entry script
```

### **GitHub Release Structure**

```
releases/
├── CHANGELOG.md                  # Version changelog
├── binary/                      # Pre-built binaries
│   ├── paper2data-linux-x64
│   ├── paper2data-macos-x64
│   └── paper2data-windows-x64.exe
└── examples/                    # Usage examples
    ├── basic_usage.md
    ├── advanced_features.md
    └── api_integration.md
```

---

This project structure is designed to support Paper2Data's evolution from a functional tool to a comprehensive, enterprise-ready academic PDF processing platform. The modular design ensures maintainability, extensibility, and scalability while providing clear separation of concerns and testability. 