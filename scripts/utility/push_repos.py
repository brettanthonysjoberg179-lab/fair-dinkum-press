import subprocess
import sys

# Get GitHub token via gh CLI
token_res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
token = token_res.stdout.strip()

if not token:
    print("Error: Could not retrieve GitHub token.", file=sys.stderr)
    sys.exit(1)

remotes = {
    "fair-dinkum": "https://github.com/brettanthonysjoberg179-lab/fair-dinkum-publishing.git",
    "origin": "https://github.com/brettanthonysjoberg179-lab/autonomous-solopreneur.git"
}

for name, url in remotes.items():
    auth_url = url.replace("https://", f"https://{token}@")
    print(f"Setting remote {name} URL and pushing...")
    subprocess.run(["git", "remote", "set-url", name, auth_url], check=True)
    push_res = subprocess.run(["git", "push", name, "master"])
    if push_res.returncode == 0:
        print(f"Successfully pushed to {name}!")
    else:
        print(f"Failed to push to {name}.", file=sys.stderr)

print("All push operations complete.")
