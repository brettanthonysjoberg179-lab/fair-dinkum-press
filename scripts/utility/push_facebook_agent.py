import subprocess

repo_name = "facebook-posting-agent"
print(f"🚀 Updating GitHub repository {repo_name}...")

subprocess.run(["git", "-C", "facebook-posting-agent", "add", "."], check=True)

res = subprocess.run(["git", "-C", "facebook-posting-agent", "diff", "--cached", "--quiet"])
if res.returncode != 0:
    subprocess.run(["git", "-C", "facebook-posting-agent", "commit", "-m", "Add image/video media generation and Meta MCP integration docs"], check=True)

token_res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
token = token_res.stdout.strip()
remote_url = f"https://brettanthonysjoberg179-lab:{token}@github.com/brettanthonysjoberg179-lab/{repo_name}.git"

subprocess.run(["git", "-C", "facebook-posting-agent", "remote", "set-url", "origin", remote_url], check=True)
subprocess.run(["git", "-C", "facebook-posting-agent", "push", "origin", "master"], check=True)

print(f"✅ Successfully pushed updates to {repo_name} on GitHub!")
