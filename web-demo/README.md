# Paper2Data Web Demo

A simple web interface for Paper2Data that allows researchers to convert academic papers to structured data repositories through their browser.

## Features

- 📄 **Upload PDF files** - Drag and drop or browse for PDF files
- 🌐 **arXiv integration** - Process papers directly from arXiv URLs
- 🔗 **DOI resolution** - Enter DOI to automatically fetch and process papers
- 📊 **Real-time processing** - See progress as your paper is analyzed
- 📦 **Downloadable results** - Get organized zip files with all extracted data

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8000`

### Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t paper2data-web .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 paper2data-web
   ```

### Deploy to Railway (Free Hosting)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set up custom domain (optional):**
   ```bash
   railway domain
   ```

### Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

## API Endpoints

### `POST /process`
Process a paper from file upload, arXiv URL, or DOI.

**Parameters:**
- `file` (multipart): PDF file (optional)
- `arxiv_url` (form): arXiv URL or ID (optional)
- `doi` (form): DOI string (optional)

**Response:**
```json
{
  "success": true,
  "session_id": "20240713_143052_123456",
  "download_url": "/download/20240713_143052_123456",
  "result_summary": {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "sections_count": 5,
    "figures_count": 3,
    "tables_count": 2
  }
}
```

### `GET /download/{session_id}`
Download the processed results as a zip file.

### `GET /status/{session_id}`
Check processing status for a session.

### `DELETE /cleanup/{session_id}`
Clean up session files.

## Output Structure

The downloaded zip file contains:
```
paper2data_results_{session_id}.zip
├── figures/           # Extracted figures with metadata
├── tables/           # Tables converted to CSV
├── sections/         # Paper sections as text files
├── metadata/         # Paper metadata (JSON)
└── README.md         # Overview of extracted content
```

## Configuration

The web demo uses the default Paper2Data configuration. For custom settings, modify the `default_config` in `main.py`.

## Security Considerations

- File uploads are limited to PDF files only
- Session files are automatically cleaned up after 24 hours
- Temporary files are stored in isolated session directories
- CORS is enabled for development (disable in production)

## Production Deployment

For production use:

1. **Disable CORS** or configure specific origins
2. **Set up HTTPS** with proper SSL certificates
3. **Configure rate limiting** to prevent abuse
4. **Set up monitoring** and logging
5. **Use external storage** (S3) for larger files
6. **Implement user authentication** if needed

## Environment Variables

- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `TEMP_DIR` - Temporary file directory
- `MAX_FILE_SIZE` - Maximum upload file size

## Cost Estimation

**Free Hosting Options:**
- Railway: 500 hours/month free
- Vercel: Unlimited for hobby projects
- Heroku: 550 hours/month free (with student pack)

**Paid Hosting (for scale):**
- Railway: $5-20/month
- DigitalOcean App Platform: $12-48/month
- AWS/GCP: $20-100/month depending on usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License - see the main Paper2Data repository for details.
