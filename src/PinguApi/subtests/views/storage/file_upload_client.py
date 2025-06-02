import io
import requests
import os
import json
import base64

# Base configuration
BASE_URL = "http://127.0.0.1:8086"  # Adjust to your server's URL
TOKEN = "25f30eb57c067f630d9529fa70ca0ef1c0e4e570"    # Replace with a valid token from your Django app
HEADERS = {
    "Authorization": f"Token {TOKEN}"
}
# Endpoint
UPLOAD_URL = f"{BASE_URL}/api/storage/dictionaries/upload/"

def upload_blob(project_id, fuzztarget_id, file_path, metadata=None):
    """
    Uploads a blob file to the server.
    
    Args:
        project_id (str): UUID of the project.
        key (str): Key for the blob in storage.
        file_path (str): Path to the file to upload.
        metadata (dict, optional): Metadata as a dictionary to be sent as JSON.
    """
    print(f"Uploading blob to project {project_id} with key {fuzztarget_id}...")

    # Validate file path
    if not os.path.isfile(file_path):
        raise ValueError(f"{file_path} is not a file or does not exist")

    # Prepare data
    data = {
        "project_id": project_id,
        "fuzztarget_id": fuzztarget_id,
    }
    
    # Add metadata if provided
    if metadata:
        data["metadata"] = json.dumps(metadata)  # Convert dict to JSON string
    
    # Prepare the file
    with open(file_path, "rb") as f:
        files = {
            "dictionary": (os.path.basename(file_path), io.BytesIO(f.read()), "text/plain")
        }
        
        try:
            # Send POST request with multipart/form-data
            response = requests.post(
                UPLOAD_URL,
                data=data,
                files=files,
                headers=HEADERS
            )
            
            # Check response
            response.raise_for_status()  # Raises exception for 4xx/5xx status codes
            print("Upload successful!")
            print(response.json())
        
        except requests.exceptions.HTTPError as e:
            print(f"Upload failed: {e}")
            if response.content:
                print(response.json())

def main():
    # Sample data (replace with real values from your database)
    project_id = "56ffb10e-7609-4634-991e-1c309879a7ba"  # Example UUID
    fuzztarget_id = "0dfc1fca-eb9b-4328-b1e9-e303d902209f"
    
    
    # Create a sample file to upload
    file_path = "test_blob.txt"
    with open(file_path, "wb") as f:
        f.write(b"Sample blob content")
    
    # Optional metadata
    metadata = {
        "description": "Test blob",
        "size": os.path.getsize(file_path)
    }
    
    # Test upload with metadata
    upload_blob(project_id, fuzztarget_id, file_path, metadata)
    
    # Test upload without metadata
    upload_blob(project_id, "another_key", file_path)
    
    # Clean up
    os.remove(file_path)
    print(f"Cleaned up {file_path}")

if __name__ == "__main__":
    main()