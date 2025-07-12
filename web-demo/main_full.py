#!/usr/bin/env python3
"""
Paper2Data Web Demo - Full Version
Uses the complete Paper2Data functionality instead of limited demo features.
"""

import os
import sys
import tempfile
import zipfile
import shutil
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

# Import Paper2Data functionality
try:
    # Try importing the locally installed package first
    import paper2data
    from paper2data import (
        create_ingestor,
        extract_all_content,
        ConfigManager,
        load_config,
        save_json,
        create_output_structure,
        get_smart_config,
        setup_logging,
        get_logger
    )
    PAPER2DATA_AVAILABLE = True
    print("✅ Paper2Data library loaded successfully (installed package)")
except ImportError as e:
    print(f"❌ Failed to import installed Paper2Data: {e}")
    # Try importing from local copy
    try:
        sys.path.insert(0, str(Path(__file__).parent / "paper2data_local"))
        import paper2data_local as paper2data
        from paper2data_local import (
            create_ingestor,
            extract_all_content,
            ConfigManager,
            load_config,
            save_json,
            create_output_structure,
            get_smart_config,
            setup_logging,
            get_logger
        )
        PAPER2DATA_AVAILABLE = True
        print("✅ Paper2Data library loaded successfully (local copy)")
    except ImportError as e2:
        print(f"❌ Failed to import local Paper2Data: {e2}")
        # Try development path as fallback
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "parser" / "src"))
            import paper2data
            from paper2data import (
                create_ingestor,
                extract_all_content,
                ConfigManager,
                load_config,
                save_json,
                create_output_structure,
                get_smart_config,
                setup_logging,
                get_logger
            )
            PAPER2DATA_AVAILABLE = True
            print("✅ Paper2Data library loaded successfully (development mode)")
        except ImportError as e3:
            print(f"❌ Failed to import Paper2Data in dev mode: {e3}")
            PAPER2DATA_AVAILABLE = False

app = FastAPI(
    title="Paper2Data Web Demo - Full Version",
    description="Complete Paper2Data functionality for extracting structured data from academic papers",
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
TEMP_DIR = Path(tempfile.gettempdir()) / "paper2data_web_full"
TEMP_DIR.mkdir(exist_ok=True)

# Setup logging for Paper2Data
if PAPER2DATA_AVAILABLE:
    setup_logging(level="INFO")
    logger = get_logger(__name__)
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main web interface"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/process")
async def process_paper(
    file: Optional[UploadFile] = File(None),
    arxiv_url: Optional[str] = Form(None),
    doi: Optional[str] = Form(None)
):
    """Process a paper using full Paper2Data functionality"""
    
    if not PAPER2DATA_AVAILABLE:
        raise HTTPException(
            status_code=500, 
            detail="Paper2Data library not available. Please install the complete package."
        )
    
    if not any([file, arxiv_url, doi]):
        raise HTTPException(status_code=400, detail="Please provide a PDF file, arXiv URL, or DOI")
    
    # Create unique session directory
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    
    try:
        # Determine input source
        input_source = None
        input_type = None
        
        if file:
            # Handle file upload
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            # Save uploaded file
            pdf_path = session_dir / "input.pdf"
            async with aiofiles.open(pdf_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            input_source = str(pdf_path)
            input_type = "pdf"
            
        elif arxiv_url:
            input_source = arxiv_url
            input_type = "arxiv"
            
        elif doi:
            input_source = doi
            input_type = "doi"
        
        # Process using Paper2Data
        logger.info(f"Processing {input_type}: {input_source}")
        result = await process_with_paper2data(input_source, session_dir)
        
        # Create downloadable zip
        zip_path = await create_result_zip(session_dir)
        
        return {
            "success": True,
            "session_id": session_id,
            "download_url": f"/download/{session_id}",
            "result_summary": result
        }
        
    except Exception as e:
        # Clean up on error
        if session_dir.exists():
            shutil.rmtree(session_dir, ignore_errors=True)
        
        # More specific error handling
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Paper not found: {str(e)}")
        elif "timeout" in str(e).lower():
            raise HTTPException(status_code=408, detail=f"Processing timeout: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

async def process_with_paper2data(input_source: str, session_dir: Path) -> dict:
    """Process paper using the full Paper2Data library"""
    
    try:
        # Get or create configuration
        config = get_smart_config()
        
        # Create ingestor for the input source
        ingestor = create_ingestor(input_source)
        
        # Validate input
        logger.info("Validating input...")
        ingestor.validate()
        
        # Ingest content (this returns PDF bytes)
        logger.info("Ingesting content...")
        pdf_content = ingestor.ingest()
        
        # Create output structure
        output_dir = session_dir / "extraction_results"
        output_dir.mkdir(exist_ok=True)
        
        # Extract all content using Paper2Data
        logger.info("Extracting content with Paper2Data...")
        extraction_results = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: extract_all_content(
                pdf_content,  # PDF bytes directly
                output_format=None,
                output_path=str(output_dir)
            )
        )
        
        # Process the extraction results
        result_summary = {
            "title": extraction_results.get("metadata", {}).get("title", "Unknown Paper"),
            "authors": extraction_results.get("metadata", {}).get("authors", []),
            "abstract": extraction_results.get("metadata", {}).get("abstract", ""),
            "sections_count": len(extraction_results.get("sections", {})),
            "figures_count": len(extraction_results.get("figures", {})),
            "tables_count": len(extraction_results.get("tables", {})),
            "citations_count": len(extraction_results.get("citations", {})),
            "equations_count": len(extraction_results.get("equations", {})),
            "pages": extraction_results.get("metadata", {}).get("page_count", 0),
            "processing_time": extraction_results.get("processing_time", 0),
            "source_type": ingestor.metadata.get("source_type", "unknown"),
            "processed_at": datetime.now().isoformat(),
            "extraction_quality": "full"
        }
        
        # Save detailed results
        save_json(extraction_results, output_dir / "complete_results.json")
        
        # Create organized output structure
        await organize_extraction_results(extraction_results, session_dir)
        
        # Create README with detailed information
        await create_detailed_readme(result_summary, extraction_results, session_dir)
        
        logger.info(f"Extraction complete: {result_summary['sections_count']} sections, "
                   f"{result_summary['figures_count']} figures, {result_summary['tables_count']} tables")
        
        return result_summary
        
    except Exception as e:
        logger.error(f"Paper2Data processing failed: {str(e)}")
        raise Exception(f"Paper2Data processing failed: {str(e)}")

async def organize_extraction_results(extraction_results: dict, session_dir: Path):
    """Organize extraction results into a clean structure"""
    
    # Create organized directory structure
    dirs = {
        "metadata": session_dir / "metadata",
        "sections": session_dir / "sections", 
        "figures": session_dir / "figures",
        "tables": session_dir / "tables",
        "citations": session_dir / "citations",
        "equations": session_dir / "equations"
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(exist_ok=True)
    
    # Save metadata
    metadata = extraction_results.get("metadata", {})
    save_json(metadata, dirs["metadata"] / "paper_metadata.json")
    
    # Save sections - handle dict or list format
    sections_data = extraction_results.get("sections", {})
    if isinstance(sections_data, dict):
        # Handle nested dict structure
        sections_list = []
        for key, value in sections_data.items():
            if isinstance(value, list):
                sections_list.extend(value)
            elif isinstance(value, dict):
                sections_list.append(value)
        
        for i, section in enumerate(sections_list):
            if isinstance(section, dict):
                section_filename = f"section_{i+1:02d}_{section.get('title', 'untitled').replace(' ', '_')[:50]}.json"
                save_json(section, dirs["sections"] / section_filename)
                
                # Also save as markdown
                md_filename = section_filename.replace('.json', '.md')
                section_md = f"# {section.get('title', 'Untitled Section')}\n\n{section.get('content', '')}"
                with open(dirs["sections"] / md_filename, "w", encoding="utf-8") as f:
                    f.write(section_md)
    elif isinstance(sections_data, list):
        for i, section in enumerate(sections_data):
            section_filename = f"section_{i+1:02d}_{section.get('title', 'untitled').replace(' ', '_')[:50]}.json"
            save_json(section, dirs["sections"] / section_filename)
            
            # Also save as markdown
            md_filename = section_filename.replace('.json', '.md')
            section_md = f"# {section.get('title', 'Untitled Section')}\n\n{section.get('content', '')}"
            with open(dirs["sections"] / md_filename, "w", encoding="utf-8") as f:
                f.write(section_md)
    
    # Save figures - handle dict or list format  
    figures_data = extraction_results.get("figures", {})
    if isinstance(figures_data, dict):
        # Extract actual figures from nested structure
        figures_list = []
        for key, value in figures_data.items():
            if isinstance(value, list):
                figures_list.extend(value)
            elif isinstance(value, dict) and "images" in value:
                figures_list.extend(value["images"])
        
        for i, figure in enumerate(figures_list):
            if isinstance(figure, dict):
                figure_filename = f"figure_{i+1:02d}.json"
                save_json(figure, dirs["figures"] / figure_filename)
                
                # Save actual image if available
                if "image_data" in figure:
                    image_filename = f"figure_{i+1:02d}.{figure.get('format', 'png')}"
                    with open(dirs["figures"] / image_filename, "wb") as f:
                        f.write(figure["image_data"])
                elif "path" in figure and Path(figure["path"]).exists():
                    # Copy existing image file
                    image_filename = f"figure_{i+1:02d}{Path(figure['path']).suffix}"
                    shutil.copy2(figure["path"], dirs["figures"] / image_filename)
    elif isinstance(figures_data, list):
        for i, figure in enumerate(figures_data):
            figure_filename = f"figure_{i+1:02d}.json"
            save_json(figure, dirs["figures"] / figure_filename)
            
            # Save actual image if available
            if "image_data" in figure:
                image_filename = f"figure_{i+1:02d}.{figure.get('format', 'png')}"
                with open(dirs["figures"] / image_filename, "wb") as f:
                    f.write(figure["image_data"])
    
    # Save tables - handle dict or list format
    tables_data = extraction_results.get("tables", {})
    if isinstance(tables_data, dict):
        # Extract actual tables from nested structure
        tables_list = []
        for key, value in tables_data.items():
            if isinstance(value, list):
                tables_list.extend(value)
            elif isinstance(value, dict) and "tables" in value:
                tables_list.extend(value["tables"])
        
        for i, table in enumerate(tables_list):
            if isinstance(table, dict):
                table_filename = f"table_{i+1:02d}.json"
                save_json(table, dirs["tables"] / table_filename)
                
                # Also save as CSV if structured data is available
                if "data" in table and isinstance(table["data"], list):
                    csv_filename = f"table_{i+1:02d}.csv"
                    import csv
                    with open(dirs["tables"] / csv_filename, "w", newline="", encoding="utf-8") as f:
                        if table["data"]:
                            writer = csv.writer(f)
                            writer.writerows(table["data"])
    elif isinstance(tables_data, list):
        for i, table in enumerate(tables_data):
            table_filename = f"table_{i+1:02d}.json"
            save_json(table, dirs["tables"] / table_filename)
            
            # Also save as CSV if structured data is available
            if "data" in table and isinstance(table["data"], list):
                csv_filename = f"table_{i+1:02d}.csv"
                import csv
                with open(dirs["tables"] / csv_filename, "w", newline="", encoding="utf-8") as f:
                    if table["data"]:
                        writer = csv.writer(f)
                        writer.writerows(table["data"])
    
    # Save citations - handle dict or list format
    citations_data = extraction_results.get("citations", {})
    if isinstance(citations_data, dict):
        save_json(citations_data, dirs["citations"] / "all_citations.json")
        
        # Extract individual citations if available
        citations_list = []
        for key, value in citations_data.items():
            if isinstance(value, list):
                citations_list.extend(value)
        
        if citations_list:
            save_json(citations_list, dirs["citations"] / "citations_list.json")
            
            # Create bibliography file
            bib_content = "# Bibliography\n\n"
            for i, citation in enumerate(citations_list):
                bib_content += f"{i+1}. {citation.get('text', 'Unknown citation')}\n"
            
            with open(dirs["citations"] / "bibliography.md", "w", encoding="utf-8") as f:
                f.write(bib_content)
    elif isinstance(citations_data, list):
        if citations_data:
            save_json(citations_data, dirs["citations"] / "all_citations.json")
            
            # Create bibliography file
            bib_content = "# Bibliography\n\n"
            for i, citation in enumerate(citations_data):
                bib_content += f"{i+1}. {citation.get('text', 'Unknown citation')}\n"
            
            with open(dirs["citations"] / "bibliography.md", "w", encoding="utf-8") as f:
                f.write(bib_content)
    
    # Save equations - handle dict or list format
    equations_data = extraction_results.get("equations", {})
    if isinstance(equations_data, dict):
        save_json(equations_data, dirs["equations"] / "all_equations.json")
        
        # Extract individual equations if available
        equations_list = equations_data.get("equations", [])
        if equations_list:
            for i, equation in enumerate(equations_list):
                eq_filename = f"equation_{i+1:02d}.json"
                save_json(equation, dirs["equations"] / eq_filename)
    elif isinstance(equations_data, list):
        if equations_data:
            save_json(equations_data, dirs["equations"] / "all_equations.json")

async def create_detailed_readme(result_summary: dict, extraction_results: dict, session_dir: Path):
    """Create a comprehensive README for the extraction results"""
    
    readme_content = f"""# Paper2Data Extraction Results

## Paper Information
- **Title**: {result_summary['title']}
- **Authors**: {', '.join(result_summary['authors']) if result_summary['authors'] else 'Unknown'}
- **Pages**: {result_summary['pages']}
- **Processing Time**: {result_summary.get('processing_time', 0):.2f} seconds
- **Processed**: {result_summary['processed_at']}

## Extraction Summary
- **Sections**: {result_summary['sections_count']} detected and extracted
- **Figures**: {result_summary['figures_count']} images extracted with metadata
- **Tables**: {result_summary['tables_count']} tables converted to structured data
- **Citations**: {result_summary['citations_count']} references identified
- **Equations**: {result_summary['equations_count']} mathematical expressions found

## File Structure

### 📁 metadata/
- `paper_metadata.json` - Complete paper metadata and bibliographic information

### 📁 sections/
- `section_XX.json` - Structured section data with content and metadata
- `section_XX.md` - Human-readable markdown version of each section

### 📁 figures/
- `figure_XX.json` - Figure metadata, captions, and analysis
- `figure_XX.png/jpg/pdf` - Extracted high-quality images

### 📁 tables/
- `table_XX.json` - Table metadata and structure information
- `table_XX.csv` - Table data in CSV format for easy analysis

### 📁 citations/
- `all_citations.json` - Complete citation database with metadata
- `bibliography.md` - Formatted bibliography

### 📁 equations/
- `all_equations.json` - Mathematical expressions with LaTeX and metadata

## Paper2Data Features Used

✅ **Advanced PDF Parsing**: Multi-layer content extraction  
✅ **Intelligent Section Detection**: Automatic document structure analysis  
✅ **High-Quality Figure Extraction**: Image processing with caption detection  
✅ **Table Structure Recognition**: Conversion to structured data formats  
✅ **Citation Network Analysis**: Reference extraction and metadata linking  
✅ **Mathematical Expression Processing**: LaTeX and MathML generation  
✅ **Metadata Enhancement**: Author disambiguation and venue identification  

## Quality Metrics
- **Extraction Quality**: {result_summary['extraction_quality']}
- **Content Coverage**: {len(extraction_results.get('sections', [])) / max(result_summary['pages'], 1) * 100:.1f}% sections per page
- **Figure Quality**: High-resolution extraction with automatic enhancement
- **Table Accuracy**: Structure-preserving conversion with validation

## Usage Notes

This extraction was performed using the complete Paper2Data toolkit. All extracted content maintains:
- Original formatting and structure
- High-quality image preservation  
- Accurate data type detection
- Comprehensive metadata linking

For more information about Paper2Data, visit: https://github.com/VinciGit00/Paper2Data

---
Generated by Paper2Data Web Demo v{result_summary.get('version', '1.1.0')}  
Full functionality powered by Paper2Data Parser v{paper2data.__version__}
"""

    with open(session_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

async def create_result_zip(session_dir: Path) -> Path:
    """Create a downloadable zip file of the results"""
    zip_path = session_dir / "paper2data_results.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from the session directory
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                if file != "paper2data_results.zip" and not file.startswith("input."):
                    file_path = Path(root) / file
                    arcname = str(file_path.relative_to(session_dir))
                    zipf.write(file_path, arcname)
    
    return zip_path

@app.get("/download/{session_id}")
async def download_results(session_id: str):
    """Download the processed results as a zip file"""
    session_dir = TEMP_DIR / session_id
    zip_path = session_dir / "paper2data_results.zip"
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="Results not found or expired")
    
    return FileResponse(
        zip_path,
        media_type='application/zip',
        filename=f"paper2data_results_{session_id}.zip",
        headers={"Content-Disposition": f"attachment; filename=paper2data_results_{session_id}.zip"}
    )

@app.get("/status/{session_id}")
async def get_status(session_id: str):
    """Get processing status for a session"""
    session_dir = TEMP_DIR / session_id
    
    if not session_dir.exists():
        return {"status": "not_found"}
    
    zip_path = session_dir / "paper2data_results.zip"
    if zip_path.exists():
        return {"status": "completed", "download_url": f"/download/{session_id}"}
    else:
        return {"status": "processing"}

@app.delete("/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up session files"""
    session_dir = TEMP_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir, ignore_errors=True)
    return {"success": True}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "service": "paper2data-web-demo-full",
        "version": "1.1.0",
        "paper2data_available": PAPER2DATA_AVAILABLE,
        "paper2data_version": paper2data.__version__ if PAPER2DATA_AVAILABLE else None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Paper2Data Web Demo API - Full Version",
        "version": "1.1.0",
        "description": "Complete Paper2Data functionality for academic paper processing",
        "paper2data_version": paper2data.__version__ if PAPER2DATA_AVAILABLE else None,
        "features": {
            "pdf_processing": "Advanced multi-layer extraction",
            "section_detection": "Intelligent document structure analysis",
            "figure_extraction": "High-quality image processing with captions",
            "table_processing": "Structure-preserving conversion to CSV/JSON",
            "citation_analysis": "Reference extraction with metadata linking",
            "equation_processing": "LaTeX and MathML generation",
            "metadata_enhancement": "Author disambiguation and venue identification"
        },
        "endpoints": {
            "process": "POST /process - Process a paper (PDF, arXiv, DOI)",
            "download": "GET /download/{session_id} - Download complete results",
            "status": "GET /status/{session_id} - Check processing status",
            "cleanup": "DELETE /cleanup/{session_id} - Clean up session"
        },
        "supported_inputs": ["PDF files", "arXiv URLs", "DOI strings"],
        "output_formats": ["JSON", "CSV", "Markdown", "High-res images"],
        "quality": "Production-grade extraction with full Paper2Data features"
    }

# Cleanup old sessions on startup
@app.on_event("startup")
async def cleanup_old_sessions():
    """Clean up sessions older than 24 hours"""
    import time
    current_time = time.time()
    
    if TEMP_DIR.exists():
        for session_dir in TEMP_DIR.iterdir():
            if session_dir.is_dir():
                # Check if older than 24 hours
                if current_time - session_dir.stat().st_mtime > 86400:  # 24 hours
                    shutil.rmtree(session_dir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway, Heroku, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Paper2Data Web Demo (Full Version)")
    print(f"📚 Paper2Data Available: {PAPER2DATA_AVAILABLE}")
    if PAPER2DATA_AVAILABLE:
        print(f"📦 Paper2Data Version: {paper2data.__version__}")
    print(f"🌐 Server: http://{host}:{port}")
    
    uvicorn.run(app, host=host, port=port)
