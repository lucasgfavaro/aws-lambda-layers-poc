import json
import time
import subprocess
import requests
import pytest
from threading import Thread


class TestLocalApi:
    """
    Test integration with SAM local API
    """
    
    @pytest.fixture(scope="class")
    def local_api_server(self):
        """Start SAM local API server in background"""
        print("\n🚀 Starting SAM local API server...")
        
        # Start SAM local start-api in background
        process = subprocess.Popen(
            ["sam", "local", "start-api", "--host", "127.0.0.1", "--port", "3001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=".",
            text=True
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if server is running
        try:
            response = requests.get("http://127.0.0.1:3001/hello-world-1", timeout=5)
            print(f"✅ SAM local API server is ready (status: {response.status_code})")
        except Exception as e:
            print(f"❌ Failed to connect to SAM local API server: {e}")
            process.terminate()
            raise
        
        yield "http://127.0.0.1:3001"
        
        # Cleanup
        print("\n🛑 Stopping SAM local API server...")
        process.terminate()
        process.wait()

    def test_hello_world_1_endpoint(self, local_api_server):
        """Test hello-world-1 endpoint"""
        response = requests.get(f"{local_api_server}/hello-world-1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "hello world 1"
        assert "sharedService" in data
        assert data["sharedService"] == "Layer working!"

    def test_hello_world_2_endpoint(self, local_api_server):
        """Test hello-world-2 endpoint"""
        response = requests.get(f"{local_api_server}/hello-world-2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "hello world 2"
        assert "sharedService" in data
        assert data["sharedService"] == "Layer working!"
