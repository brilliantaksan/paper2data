import os
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

# Import Paper2Data components
try:
    from paper2data.parser import PaperProcessor
    from paper2data.config import Config
except ImportError:
    # Try alternative import paths
    try:
        from paper2data_parser.parser import PaperProcessor
        from paper2data_parser.config import Config
    except ImportError:
        print("Warning: Could not import Paper2Data components. Running in demo mode.")
        PaperProcessor = None
        Config = None

app = FastAPI(
    title="Paper2Data Web Demo",
    description="Convert academic papers to structured data repositories",
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

# Initialize parser with default config
config_manager = ConfigManager()
default_config = config_manager.load_default_config()

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
    """Process a paper from file upload, arXiv URL, or DOI"""
    
    if not any([file, arxiv_url, doi]):
        raise HTTPException(status_code=400, detail="Please provide a PDF file, arXiv URL, or DOI")
    
    # Create unique session directory
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize parser for this session
        parser = Paper2DataParser(
            config_path=None,
            output_dir=str(session_dir)
        )
        
        if file:
            # Handle file upload
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            # Save uploaded file
            pdf_path = session_dir / "input.pdf"
            async with aiofiles.open(pdf_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Process the PDF
            result = await process_paper_file(parser, pdf_path, session_dir)
            
        elif arxiv_url:
            # Handle arXiv URL
            result = await process_arxiv_url(parser, arxiv_url, session_dir)
            
        elif doi:
            # Handle DOI
            result = await process_doi(parser, doi, session_dir)
        
        # Create downloadable zip
        zip_path = await create_result_zip(session_dir, result)
        
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
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

async def process_paper_file(parser: Paper2DataParser, pdf_path: Path, session_dir: Path):
    """Process a local PDF file"""
    result = parser.parse_document(str(pdf_path))
    return {
        "title": result.get("metadata", {}).get("title", "Unknown"),
        "authors": result.get("metadata", {}).get("authors", []),
        "sections_count": len(result.get("sections", [])),
        "figures_count": len(result.get("figures", [])),
        "tables_count": len(result.get("tables", [])),
        "output_directory": str(session_dir)
    }

async def process_arxiv_url(parser: Paper2DataParser, arxiv_url: str, session_dir: Path):
    """Process an arXiv URL"""
    # Extract arXiv ID from URL
    arxiv_id = arxiv_url.split('/')[-1]
    if '.pdf' in arxiv_id:
        arxiv_id = arxiv_id.replace('.pdf', '')
    
    result = parser.parse_arxiv(arxiv_id)
    return {
        "arxiv_id": arxiv_id,
        "title": result.get("metadata", {}).get("title", "Unknown"),
        "authors": result.get("metadata", {}).get("authors", []),
        "sections_count": len(result.get("sections", [])),
        "figures_count": len(result.get("figures", [])),
        "tables_count": len(result.get("tables", [])),
        "output_directory": str(session_dir)
    }

async def process_doi(parser: Paper2DataParser, doi: str, session_dir: Path):
    """Process a DOI"""
    result = parser.parse_doi(doi)
    return {
        "doi": doi,
        "title": result.get("metadata", {}).get("title", "Unknown"),
        "authors": result.get("metadata", {}).get("authors", []),
        "sections_count": len(result.get("sections", [])),
        "figures_count": len(result.get("figures", [])),
        "tables_count": len(result.get("tables", [])),
        "output_directory": str(session_dir)
    }

async def create_result_zip(session_dir: Path, result_summary: dict) -> Path:
    """Create a downloadable zip file of the results"""
    zip_path = session_dir / "paper2data_results.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from the output directory
        for root, dirs, files in os.walk(session_dir):
            for file in files:
                if file != "paper2data_results.zip":  # Don't include the zip itself
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

# Cleanup old sessions on startup
@app.on_event("startup")
async def cleanup_old_sessions():
    """Clean up sessions older than 24 hours"""
    import time
    current_time = time.time()
    
    for session_dir in TEMP_DIR.iterdir():
        if session_dir.is_dir():
            # Check if older than 24 hours
            if current_time - session_dir.stat().st_mtime > 86400:  # 24 hours
                shutil.rmtree(session_dir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
