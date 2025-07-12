#!/usr/bin/env python3
"""
Quick test script to debug Paper2Data import issues
"""

import sys
import traceback
from pathlib import Path

print("🔍 Testing Paper2Data imports...")

# Test 1: Try local copy
print("\n1. Testing local copy import...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "paper2data_local"))
    import paper2data_local
    print(f"✅ Local import successful: {paper2data_local.__version__}")
    
    # Test key functions
    from paper2data_local import create_ingestor, extract_all_content
    print("✅ Key functions imported successfully")
    
    # Test ingestor creation
    ingestor = create_ingestor("https://arxiv.org/abs/2301.00001")
    print(f"✅ Ingestor created: {type(ingestor)}")
    
except Exception as e:
    print(f"❌ Local import failed: {e}")
    traceback.print_exc()

# Test 2: Try installed package
print("\n2. Testing installed package import...")
try:
    import paper2data
    print(f"✅ Installed package import successful: {paper2data.__version__}")
except Exception as e:
    print(f"❌ Installed package import failed: {e}")

print("\n🔍 Python path:")
for i, path in enumerate(sys.path[:5]):
    print(f"  {i}: {path}")

print(f"\n📂 Current directory: {Path.cwd()}")
print(f"📂 Script directory: {Path(__file__).parent}")

local_path = Path(__file__).parent / "paper2data_local"
print(f"📂 Local Paper2Data path: {local_path}")
print(f"📁 Local path exists: {local_path.exists()}")

if local_path.exists():
    print(f"📁 Local path contents:")
    for item in local_path.iterdir():
        if item.is_file() and item.suffix == '.py':
            print(f"   - {item.name}")
