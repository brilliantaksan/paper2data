#!/usr/bin/env python3
"""
Test Paper2Data extraction to debug JSON serialization issues
"""

import sys
import json
import traceback
from pathlib import Path

# Set up path
sys.path.insert(0, str(Path(__file__).parent / "paper2data_local"))

try:
    from paper2data_local import create_ingestor, extract_all_content
    
    print("🔍 Testing Paper2Data extraction...")
    
    # Create ingestor
    ingestor = create_ingestor("https://arxiv.org/abs/2301.00001")
    print("✅ Ingestor created")
    
    # Validate (this might take a moment)
    print("🔍 Validating input...")
    ingestor.validate()
    print("✅ Input validated")
    
    # Ingest content (this downloads the PDF)
    print("📥 Ingesting content...")
    pdf_content = ingestor.ingest()
    print(f"✅ Content ingested: {len(pdf_content)} bytes")
    
    # Extract content (this is the main processing)
    print("🔄 Extracting content...")
    results = extract_all_content(pdf_content)
    print("✅ Content extracted")
    
    # Check what we got
    print(f"\n📊 Results structure:")
    for key, value in results.items():
        if isinstance(value, dict):
            print(f"  {key}: dict with {len(value)} items")
        elif isinstance(value, list):
            print(f"  {key}: list with {len(value)} items")
        elif isinstance(value, bytes):
            print(f"  {key}: bytes ({len(value)} bytes)")
        else:
            print(f"  {key}: {type(value)} - {str(value)[:100]}")
    
    # Test JSON serialization
    print("\n🔍 Testing JSON serialization...")
    
    def json_serializer(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, bytes):
            return f"<bytes: {len(obj)} bytes>"
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
    
    try:
        json_str = json.dumps(results, indent=2, default=json_serializer)
        print("✅ JSON serialization successful")
        print(f"📝 JSON length: {len(json_str)} characters")
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        traceback.print_exc()
        
        # Try to find the problematic object
        print("\n🔍 Checking individual keys...")
        for key, value in results.items():
            try:
                json.dumps(value, default=json_serializer)
                print(f"  ✅ {key}: OK")
            except Exception as ke:
                print(f"  ❌ {key}: {ke}")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    traceback.print_exc()
