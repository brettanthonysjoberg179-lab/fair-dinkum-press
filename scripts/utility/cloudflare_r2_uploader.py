#!/usr/bin/env python3
"""
Cloudflare R2 Asset Uploader & Signed URL Generator
Connects to Cloudflare R2 S3-compatible storage using credentials from cloudflare.env
and uploads digital products (ZIPs, PDFs, covers) for secure delivery.
"""

import os
import boto3
from botocore.config import Config

def load_cloudflare_env():
    env_path = "cloudflare.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_cloudflare_env()

ENDPOINT_URL = os.getenv("S3_API_ENDPONT")
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
BUCKET_NAME = "fair-dinkum-assets"

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

def upload_file_to_r2(local_path, object_name=None):
    if not object_name:
        object_name = os.path.basename(local_path)
    
    s3 = get_s3_client()
    try:
        print(f"[+] Uploading {local_path} to R2 bucket '{BUCKET_NAME}' as '{object_name}'...")
        s3.upload_file(local_path, BUCKET_NAME, object_name)
        
        # Generate presigned URL valid for 7 days (604800 seconds)
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=604800
        )
        print(f"[SUCCESS] Uploaded {object_name}")
        print(f"[URL] Signed Download URL: {url}")
        return url
    except Exception as e:
        print(f"[ERROR] Failed to upload {local_path}: {e}")
        return None

if __name__ == "__main__":
    print("Cloudflare R2 Asset Uploader initialized.")
    # Example upload test if package exists
    test_file = "outputs/autonomous_solopreneur_gumroad_package.zip"
    if os.path.exists(test_file):
        upload_file_to_r2(test_file)
    else:
        print(f"Test package not found at {test_file}. Run packaging scripts first.")
