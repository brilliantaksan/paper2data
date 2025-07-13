import os
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil
import json
import traceback

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

# Add the paper2data_local directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "paper2data_local"))

# Import Paper2Data components
try:
    from paper2data_local import (
        ContentExtractor,
        ConfigManager,
        Paper2DataConfig
    )
    from paper2data_local.utils import get_logger
    PAPER2DATA_AVAILABLE = True
    logger = get_logger(__name__)
    print("✅ Paper2Data library loaded successfully")
except ImportError as e:
    PAPER2DATA_AVAILABLE = False
    print(f"❌ Failed to import Paper2Data: {e}")
    traceback.print_exc()

app = FastAPI(
    title="Paper2Data Web Demo - Full Version",
    description="Convert academic papers to structured data repositories using the complete Paper2Data toolkit",
    version="1.1.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global temp directory for processing
TEMP_DIR = Path(tempfile.gettempdir()) / "paper2data_web"
TEMP_DIR.mkdir(exist_ok=True)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "paper2data-web-demo-full",
        "version": "1.1.0",
        "paper2data_available": PAPER2DATA_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main web interface"""
    with open("static/index.html", "r") as f:
        content = f.read()
        # Add a banner to indicate this is the full version
        if PAPER2DATA_AVAILABLE:
            banner = '<div style="background-color: #4CAF50; color: white; padding: 10px; text-align: center; margin-bottom: 20px;">🚀 Full Paper2Data Processing Available</div>'
        else:
            banner = '<div style="background-color: #f44336; color: white; padding: 10px; text-align: center; margin-bottom: 20px;">⚠️ Demo Mode - Paper2Data Library Not Available</div>'
        
        # Insert banner after body tag
        content = content.replace('<body>', f'<body>{banner}')
        return HTMLResponse(content=content)

@app.post("/process")
async def process_paper(
    file: Optional[UploadFile] = File(None),
    arxiv_url: Optional[str] = Form(None),
    doi: Optional[str] = Form(None)
):
    """Process a paper from file upload, arXiv URL, or DOI using full Paper2Data"""
    
    if not any([file, arxiv_url, doi]):
        raise HTTPException(status_code=400, detail="Please provide a PDF file, arXiv URL, or DOI")
    
    if not PAPER2DATA_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Paper2Data library not available. Please install the complete package."
        )
    
    # Create unique session directory
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    
    try:
        # Load default configuration
        config_manager = ConfigManager()
        config = config_manager.load_config(use_smart_defaults=True, validate=False)
        
        if file:
            # Handle file upload
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            # Save uploaded file
            pdf_path = session_dir / "input.pdf"
            async with aiofiles.open(pdf_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Process the PDF using Paper2Data
            result = await process_pdf_full(str(pdf_path), session_dir, file.filename, config)
            
        elif arxiv_url:
            # Handle arXiv URL
            result = await process_arxiv_full(arxiv_url, session_dir, config)
            
        elif doi:
            # Handle DOI
            result = await process_doi_full(doi, session_dir, config)
        
        # Create downloadable zip
        zip_path = await create_result_zip(session_dir, result)
        
        return {
            "success": True,
            "session_id": session_id,
            "download_url": f"/download/{session_id}",
            "result_summary": result,
            "processing_mode": "full"
        }
        
    except Exception as e:
        # Clean up on error
        if session_dir.exists():
            shutil.rmtree(session_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

async def process_pdf_full(pdf_path: str, session_dir: Path, filename: str, config: Paper2DataConfig):
    """Process PDF using full Paper2Data functionality"""
    try:
        # Read PDF file as bytes
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        # Use comprehensive extraction with all available extractors
        from paper2data_local.extractor import (
            ContentExtractor, SectionExtractor, FigureExtractor, 
            TableExtractor, CitationExtractor, extract_all_content
        )
        
        logger.info("Starting comprehensive PDF extraction with all extractors")
        
        # Use the comprehensive extract_all_content function
        try:
            extraction_result = extract_all_content(pdf_content)
            logger.info("Comprehensive extraction completed successfully")
        except Exception as e:
            logger.warning(f"Comprehensive extraction failed: {e}, using individual extractors")
            # Fallback to individual extractors
            extraction_result = {
                "extraction_timestamp": datetime.now().isoformat(),
                "content": {},
                "sections": {},
                "figures": {},
                "tables": {},
                "citations": {},
                "equations": {},
                "metadata": {},
                "summary": {}
            }
            
            # Content extraction
            try:
                content_extractor = ContentExtractor(pdf_content)
                extraction_result["content"] = content_extractor.extract()
                logger.info("Content extraction completed")
            except Exception as e:
                logger.error(f"Content extraction failed: {e}")
                extraction_result["content"] = {}
            
            # Section extraction
            try:
                section_extractor = SectionExtractor(pdf_content)
                extraction_result["sections"] = section_extractor.extract()
                logger.info("Section extraction completed")
            except Exception as e:
                logger.error(f"Section extraction failed: {e}")
                extraction_result["sections"] = {}
            
            # Figure extraction
            try:
                figure_extractor = FigureExtractor(pdf_content)
                extraction_result["figures"] = figure_extractor.extract()
                logger.info("Figure extraction completed")
            except Exception as e:
                logger.error(f"Figure extraction failed: {e}")
                extraction_result["figures"] = {}
            
            # Table extraction
            try:
                table_extractor = TableExtractor(pdf_content)
                extraction_result["tables"] = table_extractor.extract()
                logger.info("Table extraction completed")
            except Exception as e:
                logger.error(f"Table extraction failed: {e}")
                extraction_result["tables"] = {}
            
            # Citation extraction
            try:
                citation_extractor = CitationExtractor(pdf_content)
                extraction_result["citations"] = citation_extractor.extract()
                logger.info("Citation extraction completed")
            except Exception as e:
                logger.error(f"Citation extraction failed: {e}")
                extraction_result["citations"] = {}
            
            # Equation extraction
            try:
                from paper2data_local.equation_processor import process_equations_from_pdf
                extraction_result["equations"] = process_equations_from_pdf(pdf_content)
                logger.info("Equation extraction completed")
            except Exception as e:
                logger.warning(f"Equation extraction failed: {e}")
                extraction_result["equations"] = {}
            
            # Metadata extraction
            try:
                from paper2data_local.metadata_extractor import extract_metadata
                import tempfile
                # Create temporary file for metadata extraction
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                    tmp_file.write(pdf_content)
                    temp_file_path = tmp_file.name
                
                metadata_result = extract_metadata(temp_file_path)
                extraction_result["metadata"] = {
                    "title": metadata_result.title,
                    "authors": [{"name": author.full_name, "affiliation": author.affiliation} for author in metadata_result.authors],
                    "abstract": metadata_result.abstract,
                    "keywords": metadata_result.keywords,
                    "doi": metadata_result.doi,
                    "page_count": metadata_result.page_count,
                    "word_count": metadata_result.word_count
                }
                
                # Clean up temp file
                import os
                os.unlink(temp_file_path)
                logger.info("Metadata extraction completed")
            except Exception as e:
                logger.warning(f"Metadata extraction failed: {e}")
                extraction_result["metadata"] = {}
        
        # Create output structure in session directory
        output_dir = session_dir / "paper2data_output"
        output_dir.mkdir(exist_ok=True)
        
        # Save extraction results as JSON
        results_file = session_dir / "extraction_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            # Convert to serializable format
            serializable_result = {
                "metadata": extraction_result.get("metadata", {}),
                "sections": extraction_result.get("sections", {}),
                "figures": extraction_result.get("figures", {}),
                "tables": extraction_result.get("tables", {}),
                "citations": extraction_result.get("citations", {}),
                "equations": extraction_result.get("equations", {}),
                "total_pages": extraction_result.get("total_pages", 0),
                "processing_time": extraction_result.get("processing_time", 0),
                "summary": extraction_result.get("summary", {}),
                "content": extraction_result.get("content", {})
            }
            json.dump(serializable_result, f, indent=2, ensure_ascii=False, default=str)
        
        # Create README
        readme_content = create_readme_content(extraction_result, filename)
        readme_file = session_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Extract comprehensive statistics
        content_data = extraction_result.get("content", {})
        sections_data = extraction_result.get("sections", {})
        figures_data = extraction_result.get("figures", {})
        tables_data = extraction_result.get("tables", {})
        citations_data = extraction_result.get("citations", {})
        equations_data = extraction_result.get("equations", {})
        summary_data = extraction_result.get("summary", {})
        metadata_data = extraction_result.get("metadata", {})
        
        # Calculate counts more robustly
        sections_count = 0
        if isinstance(sections_data.get("sections"), dict):
            sections_count = len(sections_data["sections"])
        elif isinstance(sections_data.get("sections"), list):
            sections_count = len(sections_data["sections"])
        elif "section_count" in sections_data:
            sections_count = sections_data["section_count"]
        
        figures_count = 0
        if isinstance(figures_data.get("figures"), list):
            figures_count = len(figures_data["figures"])
        elif "figure_count" in figures_data:
            figures_count = figures_data["figure_count"]
        elif "images_extracted" in figures_data:
            figures_count = figures_data["images_extracted"]
        
        tables_count = 0
        if isinstance(tables_data.get("tables"), list):
            tables_count = len(tables_data["tables"])
        elif "table_count" in tables_data:
            tables_count = tables_data["table_count"]
        elif "tables_found" in tables_data:
            tables_count = tables_data["tables_found"]
        
        citations_count = 0
        if isinstance(citations_data, dict):
            citations_count = citations_data.get("reference_count", 0) or len(citations_data.get("reference_list", []))
        elif isinstance(citations_data, list):
            citations_count = len(citations_data)
        
        equations_count = 0
        if isinstance(equations_data, dict):
            equations_count = equations_data.get("total_equations", 0)
        elif isinstance(equations_data, list):
            equations_count = len(equations_data)
        
        # Get page and word counts
        total_pages = (
            content_data.get("page_count", 0) or 
            metadata_data.get("page_count", 0) or 
            summary_data.get("total_pages", 0) or 
            len(content_data.get("pages", []))
        )
        
        total_words = (
            content_data.get("word_count", 0) or 
            metadata_data.get("word_count", 0) or 
            summary_data.get("total_words", 0) or 
            len(content_data.get("full_text", "").split())
        )
        
        text_preview = content_data.get("full_text", "")[:500] if content_data.get("full_text") else ""
        
        return {
            "type": "pdf",
            "filename": filename,
            "sections_extracted": sections_count,
            "figures_extracted": figures_count,
            "tables_extracted": tables_count,
            "citations_extracted": citations_count,
            "equations_extracted": equations_count,
            "metadata": metadata_data,
            "processing_time": extraction_result.get("processing_time", 0),
            "total_pages": total_pages,
            "total_words": total_words,
            "text_preview": text_preview
        }
        
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}")
        raise Exception(f"PDF processing failed: {str(e)}")

async def process_arxiv_full(arxiv_url: str, session_dir: Path, config: Paper2DataConfig):
    """Process arXiv URL using full Paper2Data functionality"""
    try:
        # For now, return a placeholder response for arXiv
        # TODO: Implement full arXiv download and processing
        return {
            "type": "arxiv",
            "url": arxiv_url,
            "title": "arXiv processing not yet fully implemented",
            "sections_extracted": 0,
            "figures_extracted": 0,
            "tables_extracted": 0,
            "citations_extracted": 0,
            "equations_extracted": 0,
            "metadata": {"title": "arXiv processing placeholder"},
            "processing_time": 0,
            "total_pages": 0,
            "note": "arXiv processing will be implemented in the next update"
        }
        
    except Exception as e:
        raise Exception(f"arXiv processing failed: {str(e)}")

async def process_doi_full(doi: str, session_dir: Path, config: Paper2DataConfig):
    """Process DOI using full Paper2Data functionality"""
    try:
        # For now, return a placeholder response for DOI
        # TODO: Implement full DOI resolution and processing
        return {
            "type": "doi",
            "doi": doi,
            "title": "DOI processing not yet fully implemented",
            "sections_extracted": 0,
            "figures_extracted": 0,
            "tables_extracted": 0,
            "citations_extracted": 0,
            "equations_extracted": 0,
            "metadata": {"title": "DOI processing placeholder"},
            "processing_time": 0,
            "total_pages": 0,
            "note": "DOI processing will be implemented in the next update"
        }
        
    except Exception as e:
        raise Exception(f"DOI processing failed: {str(e)}")

def create_readme_content(extraction_result: dict, source: str) -> str:
    """Create README content for the extraction results"""
    metadata = extraction_result.get("metadata", {})
    
    content = f"""# Paper2Data Extraction Results

## Source
**Input**: {source}

## Paper Information
**Title**: {metadata.get("title", "N/A")}
**Authors**: {", ".join(metadata.get("authors", []))}
**Abstract**: {metadata.get("abstract", "N/A")[:500]}...

## Extraction Summary
- **Sections**: {len(extraction_result.get("sections", []))} sections extracted
- **Figures**: {len(extraction_result.get("figures", []))} figures extracted  
- **Tables**: {len(extraction_result.get("tables", []))} tables extracted
- **Citations**: {len(extraction_result.get("citations", []))} citations extracted
- **Equations**: {len(extraction_result.get("equations", []))} equations extracted
- **Total Pages**: {extraction_result.get("total_pages", "N/A")}
- **Processing Time**: {extraction_result.get("processing_time", 0):.2f} seconds

## Files Structure
```
paper2data_output/
├── extraction_results.json    # Complete extraction data
├── README.md                 # This file
├── figures/                  # Extracted figures
├── tables/                   # Extracted tables  
├── sections/                 # Text sections
└── metadata/                 # Paper metadata
```

## Usage
The extracted data is available in structured JSON format in `extraction_results.json`.
Individual components are organized in their respective directories.

## Paper2Data
Generated using Paper2Data v1.1.0 - https://github.com/VinciGit00/Paper2Data
"""
    return content

async def create_result_zip(session_dir: Path, result: dict):
    """Create a downloadable zip file with all results"""
    zip_path = session_dir / "paper2data_results.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files in the session directory
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                if file != "paper2data_results.zip":  # Don't include the zip itself
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(session_dir)
                    zipf.write(file_path, arcname)
    
    return zip_path

@app.get("/download/{session_id}")
async def download_results(session_id: str):
    """Download the processing results as a zip file"""
    session_dir = TEMP_DIR / session_id
    zip_path = session_dir / "paper2data_results.zip"
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    
    return FileResponse(
        path=zip_path,
        filename=f"paper2data_results_{session_id}.zip",
        media_type="application/zip"
    )

@app.get("/status")
async def get_status():
    """Get the current status of the application"""
    return {
        "service": "Paper2Data Web Demo - Full Version",
        "version": "1.1.0",
        "paper2data_available": PAPER2DATA_AVAILABLE,
        "features": {
            "pdf_processing": PAPER2DATA_AVAILABLE,
            "arxiv_processing": PAPER2DATA_AVAILABLE,
            "doi_processing": PAPER2DATA_AVAILABLE,
            "full_extraction": PAPER2DATA_AVAILABLE,
            "advanced_figures": PAPER2DATA_AVAILABLE,
            "equation_processing": PAPER2DATA_AVAILABLE,
            "citation_network": PAPER2DATA_AVAILABLE
        },
        "temp_dir": str(TEMP_DIR),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
