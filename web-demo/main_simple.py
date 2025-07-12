import os
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil
import subprocess
import json

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

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
            result = await process_pdf_demo(str(pdf_path), session_dir, file.filename)
            
        elif arxiv_url:
            # Handle arXiv URL
            result = await process_arxiv_demo(arxiv_url, session_dir)
            
        elif doi:
            # Handle DOI
            result = await process_doi_demo(doi, session_dir)
        
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
        raise HTTPException(status_code=400, detail=str(e))

async def process_pdf_demo(pdf_path: str, session_dir: Path, filename: str):
    """Process a PDF file with demo functionality"""
    try:
        # Create directory structure
        (session_dir / "metadata").mkdir(exist_ok=True)
        (session_dir / "sections").mkdir(exist_ok=True)
        (session_dir / "figures").mkdir(exist_ok=True)
        (session_dir / "tables").mkdir(exist_ok=True)
        
        # Try to extract basic info using PyMuPDF if available
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            
            # Extract metadata
            metadata = doc.metadata
            title = metadata.get('title', filename.replace('.pdf', ''))
            author = metadata.get('author', 'Unknown Author')
            
            # Extract text from first few pages
            text = ""
            for page_num in range(min(5, doc.page_count)):
                page = doc[page_num]
                text += page.get_text()
            
            # Try to extract figures
            figures_count = 0
            for page_num in range(min(doc.page_count, 10)):  # First 10 pages
                page = doc[page_num]
                image_list = page.get_images()
                figures_count += len(image_list)
            
            doc.close()
            
        except ImportError:
            # Fallback without PyMuPDF
            title = filename.replace('.pdf', '')
            author = 'Unknown Author'
            text = "PDF processing requires PyMuPDF library for full functionality."
            figures_count = 0
        
        # Create basic metadata
        result = {
            "title": title,
            "authors": [author] if author != 'Unknown Author' else [],
            "sections_count": min(len(text.split('\n\n')), 10),  # Estimate sections
            "figures_count": figures_count,
            "tables_count": text.lower().count('table') + text.lower().count('tab.'),
            "pages": len(text) // 3000 + 1,  # Rough page estimate
            "file_size": len(text),
            "processed_at": datetime.now().isoformat()
        }
        
        # Save metadata
        with open(session_dir / "metadata" / "basic_info.json", "w") as f:
            json.dump(result, f, indent=2)
        
        # Save extracted text (first 5000 characters)
        with open(session_dir / "sections" / "extracted_text.txt", "w", encoding='utf-8') as f:
            f.write(text[:5000])
        
        # Create README
        readme_content = f"""# Paper Processing Results

## {title}

**Authors:** {', '.join(result['authors']) if result['authors'] else 'Unknown'}  
**Pages:** {result['pages']}  
**Figures:** {result['figures_count']}  
**Tables:** {result['tables_count']}  

## Structure
- `metadata/` - Paper metadata and bibliographic information
- `sections/` - Extracted text content organized by sections  
- `figures/` - Extracted figures and images
- `tables/` - Extracted tables in CSV format

## Demo Note
This is a demo version of Paper2Data. The full version provides:
- Complete section detection and organization
- High-quality figure extraction  
- Table structure recognition
- Citation network analysis
- Multiple output formats

Visit https://github.com/VinciGit00/Paper2Data for the complete toolkit.
"""
        
        with open(session_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        return result
        
    except Exception as e:
        # Create minimal demo result
        return await create_demo_result(f"PDF: {filename}", session_dir)

async def process_arxiv_demo(arxiv_url: str, session_dir: Path):
    """Process an arXiv URL with demo functionality"""
    try:
        # Extract arXiv ID from URL
        arxiv_id = arxiv_url.split('/')[-1]
        if '.pdf' in arxiv_id:
            arxiv_id = arxiv_id.replace('.pdf', '')
        
        # Create directory structure
        (session_dir / "metadata").mkdir(exist_ok=True)
        (session_dir / "sections").mkdir(exist_ok=True)
        (session_dir / "figures").mkdir(exist_ok=True)
        (session_dir / "tables").mkdir(exist_ok=True)
        
        # Try to download and process from arXiv
        try:
            import requests
            
            # Get arXiv paper info via API
            api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200 and 'entry' in response.text:
                # Parse basic info from API response
                title = "arXiv Paper"
                authors = ["arXiv Author"]
                
                # Try to extract title and authors from XML
                if '<title>' in response.text:
                    title_start = response.text.find('<title>') + 7
                    title_end = response.text.find('</title>', title_start)
                    title = response.text[title_start:title_end].strip()
                
                if '<name>' in response.text:
                    authors = []
                    current_pos = 0
                    while True:
                        name_start = response.text.find('<name>', current_pos)
                        if name_start == -1:
                            break
                        name_start += 6
                        name_end = response.text.find('</name>', name_start)
                        if name_end == -1:
                            break
                        authors.append(response.text[name_start:name_end].strip())
                        current_pos = name_end
                
                result = {
                    "title": title,
                    "authors": authors,
                    "arxiv_id": arxiv_id,
                    "sections_count": 8,  # Typical academic paper
                    "figures_count": 5,
                    "tables_count": 3,
                    "pages": 12,
                    "source": "arXiv",
                    "processed_at": datetime.now().isoformat()
                }
            else:
                raise Exception("Could not fetch arXiv paper")
                
        except Exception:
            # Fallback demo result
            result = {
                "title": f"arXiv Paper {arxiv_id}",
                "authors": ["Demo Author"],
                "arxiv_id": arxiv_id,
                "sections_count": 6,
                "figures_count": 4,
                "tables_count": 2,
                "pages": 10,
                "source": "arXiv",
                "processed_at": datetime.now().isoformat()
            }
        
        # Save metadata
        with open(session_dir / "metadata" / "arxiv_info.json", "w") as f:
            json.dump(result, f, indent=2)
        
        # Create demo content
        demo_content = f"""# {result['title']}

## Abstract
This is a demo extraction from arXiv paper {arxiv_id}. 

## Authors
{', '.join(result['authors'])}

## Key Sections
1. Introduction
2. Related Work  
3. Methodology
4. Experiments
5. Results
6. Conclusion

## Demo Note
This is a simplified demo. The full Paper2Data toolkit can:
- Download and process the actual PDF from arXiv
- Extract complete text with proper section detection
- Identify and extract all figures and tables
- Analyze citation networks
- Generate structured metadata

Visit the full Paper2Data project for complete functionality.
"""
        
        with open(session_dir / "sections" / "demo_content.md", "w") as f:
            f.write(demo_content)
        
        return result
        
    except Exception as e:
        return await create_demo_result(f"arXiv: {arxiv_url}", session_dir)

async def process_doi_demo(doi: str, session_dir: Path):
    """Process a DOI with demo functionality"""
    try:
        # Create directory structure
        (session_dir / "metadata").mkdir(exist_ok=True)
        (session_dir / "sections").mkdir(exist_ok=True)
        (session_dir / "figures").mkdir(exist_ok=True)
        (session_dir / "tables").mkdir(exist_ok=True)
        
        # Try to get basic info from DOI
        try:
            import requests
            
            # Try to resolve DOI
            doi_url = f"https://doi.org/{doi}" if not doi.startswith('http') else doi
            headers = {'Accept': 'application/json'}
            response = requests.get(doi_url, headers=headers, timeout=10, allow_redirects=True)
            
            title = f"Paper with DOI {doi}"
            authors = ["DOI Author"]
            
        except Exception:
            title = f"Paper with DOI {doi}"
            authors = ["Demo Author"]
        
        result = {
            "title": title,
            "authors": authors,
            "doi": doi,
            "sections_count": 7,
            "figures_count": 6,
            "tables_count": 4,
            "pages": 15,
            "source": "DOI",
            "processed_at": datetime.now().isoformat()
        }
        
        # Save metadata
        with open(session_dir / "metadata" / "doi_info.json", "w") as f:
            json.dump(result, f, indent=2)
        
        # Create demo content
        demo_content = f"""# {result['title']}

## Metadata
- **DOI:** {doi}
- **Authors:** {', '.join(result['authors'])}
- **Estimated Pages:** {result['pages']}

## Structure Analysis
- **Sections:** {result['sections_count']} detected
- **Figures:** {result['figures_count']} identified  
- **Tables:** {result['tables_count']} found

## Demo Note
This is a demo extraction for DOI {doi}.

The full Paper2Data system can:
- Resolve DOIs to download actual PDFs
- Perform complete structural analysis
- Extract high-quality figures and tables
- Generate comprehensive metadata
- Create citation networks

For full functionality, visit the Paper2Data GitHub repository.
"""
        
        with open(session_dir / "sections" / "doi_analysis.md", "w") as f:
            f.write(demo_content)
        
        return result
        
    except Exception as e:
        return await create_demo_result(f"DOI: {doi}", session_dir)

async def extract_basic_pdf_info(pdf_path: str, session_dir: Path):
    """Extract basic information from PDF as fallback"""
    try:
        import fitz  # PyMuPDF
        
        # Create basic directory structure
        (session_dir / "metadata").mkdir(exist_ok=True)
        (session_dir / "sections").mkdir(exist_ok=True)
        (session_dir / "figures").mkdir(exist_ok=True)
        (session_dir / "tables").mkdir(exist_ok=True)
        
        doc = fitz.open(pdf_path)
        
        # Extract basic metadata
        metadata = doc.metadata
        title = metadata.get('title', 'Unknown Paper')
        author = metadata.get('author', 'Unknown Author')
        
        # Extract text from first few pages for demo
        text = ""
        for page_num in range(min(3, doc.page_count)):
            page = doc[page_num]
            text += page.get_text()
        
        # Save basic metadata
        basic_metadata = {
            "title": title,
            "authors": [author] if author else [],
            "pages": doc.page_count,
            "created": str(datetime.now())
        }
        
        with open(session_dir / "metadata" / "basic_info.json", "w") as f:
            json.dump(basic_metadata, f, indent=2)
        
        # Save extracted text
        with open(session_dir / "sections" / "extracted_text.txt", "w") as f:
            f.write(text[:2000])  # First 2000 characters
        
        # Create README
        readme_content = f"""# Paper Processing Results

## Metadata
- **Title**: {title}
- **Author**: {author}
- **Pages**: {doc.page_count}

## Note
This is a demo extraction. For full processing capabilities, 
please install Paper2Data CLI or use the complete processing pipeline.

## Files Included
- `metadata/basic_info.json` - Basic paper metadata
- `sections/extracted_text.txt` - Sample extracted text
"""
        
        with open(session_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        doc.close()
        
        return {
            "title": title,
            "authors": [author] if author else [],
            "sections_count": 1,
            "figures_count": 0,
            "tables_count": 0,
            "output_directory": str(session_dir)
        }
        
    except Exception as e:
        return create_demo_result("PDF Upload", session_dir)

async def create_demo_result(source: str, session_dir: Path):
    """Create a demo result structure"""
    # Create basic directory structure
    (session_dir / "metadata").mkdir(exist_ok=True)
    (session_dir / "sections").mkdir(exist_ok=True)
    (session_dir / "figures").mkdir(exist_ok=True)
    (session_dir / "tables").mkdir(exist_ok=True)
    
    # Create demo content
    demo_metadata = {
        "title": f"Demo Processing Result for {source}",
        "authors": ["Demo Author"],
        "source": source,
        "sections_count": 5,
        "figures_count": 3,
        "tables_count": 2,
        "pages": 8,
        "processed_at": datetime.now().isoformat(),
        "note": "This is a demonstration. For full processing, install Paper2Data CLI."
    }
    
    with open(session_dir / "metadata" / "demo_info.json", "w") as f:
        json.dump(demo_metadata, f, indent=2)
    
    readme_content = f"""# Paper2Data Demo Result

## Source
{source}

## Demo Note
This is a demonstration of the Paper2Data web interface. 

To get full processing capabilities:
1. Install Paper2Data CLI: `pip install paper2data-parser`
2. Use the command line: `paper2data process your_paper.pdf`
3. Or integrate the Python API into your projects

## What Paper2Data Can Extract
- ✅ Structured sections (Abstract, Introduction, Methods, Results, Conclusion)
- ✅ High-quality figures with captions
- ✅ Tables converted to CSV format
- ✅ Rich metadata (authors, citations, keywords)
- ✅ Mathematical equations and formulas
- ✅ References and bibliography

Visit https://github.com/VinciGit00/Paper2Data for the complete toolkit.
"""
    
    with open(session_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    return demo_metadata

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

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "service": "paper2data-web-demo",
        "version": "1.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Paper2Data Web Demo API",
        "version": "1.1.0",
        "description": "Convert academic papers to structured data repositories",
        "endpoints": {
            "process": "POST /process - Process a paper (PDF, arXiv, DOI)",
            "download": "GET /download/{session_id} - Download results",
            "status": "GET /status/{session_id} - Check processing status",
            "cleanup": "DELETE /cleanup/{session_id} - Clean up session"
        },
        "supported_inputs": ["PDF files", "arXiv URLs", "DOI strings"],
        "output_format": "ZIP file with structured data"
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
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway, Heroku, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port)
    
    # Get port from environment variable (Railway, Heroku, etc.)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port)
