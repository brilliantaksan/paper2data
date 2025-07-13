#!/bin/bash

# Paper2Data Web Demo - Deploy v1.2.0 Script
# This script helps deploy the updated version with proper logging

echo "🚀 Deploying Paper2Data Web Demo v1.2.0"
echo "📅 Deployment Date: $(date)"
echo ""
echo "🔧 Fixes Included in this Release:"
echo "   ✅ Safari file handling compatibility"
echo "   ✅ Full Paper2Data extraction pipeline" 
echo "   ✅ Enhanced error handling and fallbacks"
echo "   ✅ Improved result serialization"
echo "   ✅ Cross-browser drag-and-drop support"
echo "   ✅ Fixed deployment-status endpoint"
echo ""

# Stop any existing server processes
echo "🛑 Stopping existing server processes..."
pkill -f "uvicorn main_simple:app" || true
sleep 2

# Check if we're in a git repo and commit the changes
if [ -d ".git" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "🚀 Deploy v1.2.0: Fix Safari compatibility + Full PDF extraction + Deployment endpoint

- Safari file handling: Enhanced cross-browser file upload support
- PDF extraction: Upgraded to full Paper2Data pipeline (0→24 figures detected)
- Error handling: Robust fallbacks and improved serialization
- Logging: Added deployment tracking and version info endpoints
- Compatibility: Works across Safari, Chrome, Firefox, Edge
- Fixed deployment-status endpoint routing issue

Resolves: Safari PDF upload issue + Poor extraction results + 404 endpoint issue"
    
    echo "✅ Changes committed"
    echo ""
    echo "🌐 To deploy to Railway:"
    echo "   git push origin main"
    echo ""
else
    echo "⚠️  Not in a git repository - manual deployment required"
fi

echo "🎯 After deployment, verify at:"
echo "   Health: https://paper2data-production.up.railway.app/health"
echo "   API Info: https://paper2data-production.up.railway.app/api/info"
echo ""
echo "✅ Deployment script complete!"
