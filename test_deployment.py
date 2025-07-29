#!/usr/bin/env python3
"""
Test script for Fly.io deployment
Created by Syed Fahim
"""

import requests
import time
import sys

def test_health_endpoint(url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{url}/api/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_main_endpoint(url):
    """Test the main endpoint"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Main endpoint working: {response.status_code}")
            return True
        else:
            print(f"❌ Main endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main endpoint error: {e}")
        return False

def main():
    """Main test function"""
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <app-url>")
        print("Example: python test_deployment.py https://autonomous-task-bot.fly.dev")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    print(f"🧪 Testing deployment at: {url}")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint(url)
    
    # Test main endpoint
    print("\n2. Testing main endpoint...")
    main_ok = test_main_endpoint(url)
    
    # Summary
    print("\n" + "="*50)
    if health_ok and main_ok:
        print("🎉 All tests passed! Deployment is working correctly.")
    else:
        print("❌ Some tests failed. Check the deployment logs.")
        print("Run: fly logs --app your-app-name")
    
    print("="*50)

if __name__ == "__main__":
    main() 