#!/usr/bin/env python3
"""
Test script to verify the full Paper2Data web application functionality
"""

import requests
import json
from pathlib import Path

def test_local_app():
    """Test the local application"""
    print("🧪 Testing Local Application...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        health_data = response.json()
        print(f"✅ Health Check: {health_data['status']}")
        print(f"✅ Paper2Data Available: {health_data['paper2data_available']}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False
    
    # Test status endpoint
    try:
        response = requests.get("http://localhost:8000/status")
        status_data = response.json()
        print(f"✅ Service: {status_data['service']}")
        features = status_data['features']
        for feature, available in features.items():
            status = "✅" if available else "❌"
            print(f"{status} {feature}: {available}")
    except Exception as e:
        print(f"❌ Status Check Failed: {e}")
        return False
    
    return True

def test_railway_app():
    """Test the Railway application"""
    print("\n🚀 Testing Railway Application...")
    
    # Test health endpoint
    try:
        response = requests.get("https://paper2data-production.up.railway.app/health")
        health_data = response.json()
        print(f"✅ Health Check: {health_data['status']}")
        print(f"✅ Paper2Data Available: {health_data['paper2data_available']}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False
    
    # Test status endpoint
    try:
        response = requests.get("https://paper2data-production.up.railway.app/status")
        status_data = response.json()
        print(f"✅ Service: {status_data['service']}")
        features = status_data['features']
        for feature, available in features.items():
            status = "✅" if available else "❌"
            print(f"{status} {feature}: {available}")
    except Exception as e:
        print(f"❌ Status Check Failed: {e}")
        return False
    
    return True

def test_arxiv_processing():
    """Test arXiv processing functionality"""
    print("\n📄 Testing arXiv Processing...")
    
    # Test with a sample arXiv URL
    arxiv_url = "https://arxiv.org/abs/2301.07041"  # A sample paper
    
    try:
        data = {"arxiv_url": arxiv_url}
        response = requests.post("http://localhost:8000/process", data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ arXiv processing successful!")
                print(f"✅ Session ID: {result['session_id']}")
                print(f"✅ Download URL: {result['download_url']}")
                summary = result['result_summary']
                print(f"✅ Sections: {summary['sections_extracted']}")
                print(f"✅ Figures: {summary['figures_extracted']}")
                print(f"✅ Tables: {summary['tables_extracted']}")
                print(f"✅ Citations: {summary['citations_extracted']}")
                return True
            else:
                print(f"❌ Processing failed: {result}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ arXiv Processing Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Paper2Data Full Version Test Suite")
    print("=" * 50)
    
    local_ok = test_local_app()
    railway_ok = test_railway_app()
    
    if local_ok:
        arxiv_ok = test_arxiv_processing()
    else:
        arxiv_ok = False
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Local App: {'✅ PASS' if local_ok else '❌ FAIL'}")
    print(f"Railway App: {'✅ PASS' if railway_ok else '❌ FAIL'}")
    print(f"arXiv Processing: {'✅ PASS' if arxiv_ok else '❌ FAIL'}")
    
    if all([local_ok, railway_ok, arxiv_ok]):
        print("\n🎉 All tests passed! Full functionality is working!")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
