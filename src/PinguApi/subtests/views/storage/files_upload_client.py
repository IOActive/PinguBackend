import requests
import os
import zipfile
import io

# Base configuration
BASE_URL = "http://127.0.0.1:8086"  # Adjust to your server's URL
TOKEN = "25f30eb57c067f630d9529fa70ca0ef1c0e4e570"    # Replace with a valid token from your Django app
HEADERS = {
    "Authorization": f"Token {TOKEN}"
}

# Endpoints
UPLOAD_URL = f"{BASE_URL}/api/storage/logs/upload/"
DOWNLOAD_URL = f"{BASE_URL}/api/storage/build/download/"

def upload_corpus(project_id, fuzz_target_id, files):
    """
    Uploads corpus files to the server.
    Args:
        project_id (str): UUID of the project.
        fuzz_target_id (str): UUID of the fuzz target.
        files (list): List of file paths to upload.
    """
    print(f"Uploading files to project {project_id}, fuzz_target {fuzz_target_id}...")
    
    # Prepare data
    data = {
        "project_id": project_id,
        "task_id": "00ebe79d-8189-40aa-b42d-50fce3340468",
        "job_id": "83e5a847-053a-4309-a4b4-4eae9881c844",
        "log_type": 'bot'
    }
    
    # Prepare files (open in binary mode)
    file_objects = [("files", (os.path.basename(f), open(f, "rb"), "text/plain")) for f in files]
    
    try:
        # Send POST request with multipart/form-data
        response = requests.post(
            UPLOAD_URL,
            data=data,
            files=file_objects,
            headers=HEADERS
        )
        
        # Check response
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        print("Upload successful!")
        print(response.json())
    
    except requests.exceptions.HTTPError as e:
        print(f"Upload failed: {e}")
        print(response.json())
    
    finally:
        # Clean up file handles
        for _, (_, file_obj, _) in file_objects:
            file_obj.close()

def download_corpus(project_id, fuzz_target_id, output_dir="downloaded_corpus"):
    """
    Downloads corpus files as a ZIP and extracts them.
    Args:
        project_id (str): UUID of the project.
        fuzz_target_id (str): UUID of the fuzz target.
        output_dir (str): Directory to save and extract the downloaded files.
    """
    print(f"Downloading corpus for project {project_id}, fuzz_target {fuzz_target_id}...")
    
    # Prepare query parameters
    params = {
        "project_id": project_id,
        "build_type": "release",
        "file_path": "test-2.zip"
    }
    
    try:
        # Send GET request
        response = requests.post(
            DOWNLOAD_URL,
            data=params,
            headers=HEADERS,
            stream=True  # Enable streaming for large files
        )
        
        # Check response
        response.raise_for_status()
        
        # Get filename from Content-Disposition header (optional)
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = content_disposition.split("filename=")[-1].strip('"') if "filename=" in content_disposition else "corpus.zip"
        
        # Save the ZIP file
        os.makedirs(output_dir, exist_ok=True)
        zip_path = os.path.join(output_dir, filename)
        
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        
        print(f"Downloaded ZIP to {zip_path}")
        
        # Extract the ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
            print(f"Extracted files to {output_dir}: {zip_ref.namelist()}")
        
        # Optionally remove the ZIP file after extraction
        # os.remove(zip_path)
        # print(f"Cleaned up {zip_path}")
    
    except requests.exceptions.HTTPError as e:
        print(f"Download failed: {e}")
        if response.content:
            print(response.json())
    except zipfile.BadZipFile as e:
        print(f"Failed to extract ZIP: {e}")

def main():
    # Sample data (replace with real UUIDs from your database)
    project_id = "56ffb10e-7609-4634-991e-1c309879a7ba"
    fuzz_target_id = "0dfc1fca-eb9b-4328-b1e9-e303d902209f"
    
    # Create sample files for upload
    files_to_upload = ["src/PinguApi/subtests/test_data/corpus/testfile1.txt", "src/PinguApi/subtests/test_data/corpus/testfile2.txt"]
    for filename in files_to_upload:
        with open(filename, "w") as f:
            f.write(f"Content for {filename}")
    
    # Test upload
    upload_corpus(project_id, fuzz_target_id, files_to_upload)
    
    # Test download
    #download_corpus(project_id, fuzz_target_id, output_dir="downloaded_corpus")
    
    # Clean up sample files
    for filename in files_to_upload:
        os.remove(filename)

if __name__ == "__main__":
    main()