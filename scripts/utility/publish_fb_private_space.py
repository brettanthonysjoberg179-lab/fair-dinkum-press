from huggingface_hub import HfApi, create_repo
import os

repo_id = "Brettapps/facebook-agent-space"
print(f"🚀 Creating and publishing Private Hugging Face Space: {repo_id}...")

api = HfApi()

try:
    create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="static",
        private=True,
        exist_ok=True
    )
    print(f"✅ Private Space repository {repo_id} created/verified successfully.")
except Exception as e:
    print(f"ℹ️ Repo creation notice: {e}")

print("Uploading files from facebook-agent-space/ folder...")
api.upload_folder(
    folder_path="facebook-agent-space",
    repo_id=repo_id,
    repo_type="space",
    commit_message="Publish Private Facebook Posting Agent Control Center"
)

print(f"✅ Successfully published! Private Space URL: https://huggingface.co/spaces/{repo_id}")
