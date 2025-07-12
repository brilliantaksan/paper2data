# Paper2Data Web Demo - Deployment Guide

## Overview

This guide covers multiple deployment options for the Paper2Data web demo, from local development to production hosting.

## 🚀 Quick Local Start

```bash
cd web-demo
./start.sh
```

Then open http://localhost:8000 in your browser.

## 📦 Deployment Options

### 1. Railway (Recommended for beginners)

**Cost**: Free tier available (500 hours/month)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   cd web-demo
   railway login
   railway init
   railway up
   ```

3. **Get your URL**:
   ```bash
   railway status
   ```

### 2. Vercel (Good for static + serverless)

**Cost**: Free for personal projects

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd web-demo
   vercel
   ```

### 3. DigitalOcean App Platform

**Cost**: $12-48/month

1. **Create new app** at https://cloud.digitalocean.com/apps
2. **Connect GitHub repository**
3. **Select** `web-demo` directory
4. **Configure** build settings:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python main_simple.py`

### 4. AWS (Advanced)

**Cost**: Variable ($20-100/month depending on usage)

#### Option A: AWS App Runner
1. **Create App Runner service** in AWS Console
2. **Connect to repository**
3. **Configure**:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main_simple.py`

#### Option B: ECS with Fargate
1. **Build Docker image**:
   ```bash
   docker build -t paper2data-web .
   ```

2. **Push to ECR**:
   ```bash
   aws ecr create-repository --repository-name paper2data-web
   # Follow ECR push commands
   ```

3. **Create ECS task definition and service**

### 5. Google Cloud Platform

**Cost**: Variable ($20-80/month)

#### Option A: Cloud Run (Recommended)
1. **Build and deploy**:
   ```bash
   gcloud run deploy paper2data-web \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```

#### Option B: App Engine
1. **Create** `app.yaml`:
   ```yaml
   runtime: python311
   entrypoint: python main_simple.py
   ```

2. **Deploy**:
   ```bash
   gcloud app deploy
   ```

### 6. Heroku

**Cost**: $7-25/month

1. **Install Heroku CLI**
2. **Create Procfile**:
   ```
   web: python main_simple.py
   ```

3. **Deploy**:
   ```bash
   heroku create paper2data-web-demo
   git push heroku main
   ```

### 7. Self-hosted VPS

**Cost**: $5-20/month

1. **Setup server** (Ubuntu/Debian):
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip nginx
   
   # Clone repository
   git clone <your-repo>
   cd paper2data/web-demo
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   
   # Install PM2 for process management
   sudo npm install -g pm2
   ```

2. **Create PM2 ecosystem file**:
   ```javascript
   // ecosystem.config.js
   module.exports = {
     apps: [{
       name: 'paper2data-web',
       script: 'main_simple.py',
       interpreter: 'python3',
       env: {
         PORT: 8000
       }
     }]
   }
   ```

3. **Start with PM2**:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

4. **Configure Nginx**:
   ```nginx
   # /etc/nginx/sites-available/paper2data
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/paper2data /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 🔒 Production Considerations

### Security
- **Disable CORS** for production or configure specific origins
- **Add rate limiting** to prevent abuse
- **Use HTTPS** with SSL certificates (Let's Encrypt)
- **Validate file uploads** more strictly
- **Implement authentication** if needed

### Performance
- **Use Redis** for session storage instead of filesystem
- **Add CDN** for static assets
- **Implement caching** for frequently processed papers
- **Use S3 or similar** for file storage

### Monitoring
- **Add logging** with structured logs
- **Set up monitoring** (Datadog, New Relic, etc.)
- **Configure alerts** for errors and performance
- **Track usage metrics**

### Scaling
- **Use load balancers** for multiple instances
- **Implement queue system** (Celery + Redis) for long-running tasks
- **Add database** for persistent data
- **Consider microservices** architecture

## 📊 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Railway | 500 hours/month | $5-20/month | Beginners |
| Vercel | Unlimited hobby | $20-40/month | Static + API |
| DigitalOcean | - | $12-48/month | Full control |
| AWS | Limited free | $20-100/month | Enterprise |
| GCP | $300 credit | $20-80/month | Integration |
| Heroku | 550 hours/month | $7-25/month | Simple apps |
| VPS | - | $5-20/month | Custom setup |

## 🛠️ Environment Variables

Set these in your deployment platform:

```bash
# Optional configurations
PORT=8000                    # Server port
HOST=0.0.0.0                # Server host
MAX_FILE_SIZE=100MB         # Maximum upload size
SESSION_TIMEOUT=3600        # Session timeout (seconds)
TEMP_CLEANUP_HOURS=24       # Hours before cleanup
```

## 🚨 Troubleshooting

### Common Issues

1. **Memory errors with large PDFs**:
   - Increase memory limits in deployment platform
   - Add file size validation

2. **Timeout issues**:
   - Increase request timeout
   - Implement background processing

3. **Storage issues**:
   - Use external storage (S3, Google Cloud Storage)
   - Implement aggressive cleanup

4. **Import errors**:
   - Ensure all dependencies in requirements.txt
   - Check Python version compatibility

### Debug Mode

Add this to enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Full docs at your repository
- **Community**: Join discussions and get help

## 🚀 Next Steps

After deploying:

1. **Test thoroughly** with different paper types
2. **Monitor performance** and usage
3. **Gather user feedback**
4. **Plan scaling** based on usage patterns
5. **Consider premium features** for sustainability
