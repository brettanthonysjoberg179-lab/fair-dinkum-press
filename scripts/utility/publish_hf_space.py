from huggingface_hub import HfApi, create_repo
import os

repo_id = "Brettapps/agentkit-space"
print(f"🚀 Creating and publishing Hugging Face Static Space: {repo_id}...")

api = HfApi()

try:
    create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="static",
        private=False,
        exist_ok=True
    )
    print(f"✅ Static Space repository {repo_id} created/verified successfully.")
except Exception as e:
    print(f"ℹ️ Repo creation notice: {e}")

print("Uploading files from agentkit-space/ folder...")
api.upload_folder(
    folder_path="agentkit-space",
    repo_id=repo_id,
    repo_type="space",
    commit_message="Publish AgentKit Shop Static HTML demo showcase"
)

print(f"✅ Successfully published! Demo URL: https://huggingface.co/spaces/{repo_id}")
