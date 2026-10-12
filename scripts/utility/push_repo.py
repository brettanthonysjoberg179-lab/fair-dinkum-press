import subprocess

token_res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
token = token_res.stdout.strip()

remote_url = f"https://brettanthonysjoberg179-lab:{token}@github.com/brettanthonysjoberg179-lab/agentkit-lead-triage.git"

subprocess.run(["git", "-C", "agentkit-lead-triage", "remote", "set-url", "origin", remote_url], check=True)
subprocess.run(["git", "-C", "agentkit-lead-triage", "pull", "origin", "master", "--rebase"], check=True)
subprocess.run(["git", "-C", "agentkit-lead-triage", "add", "triage.py"], check=True)
# commit if there are changes staged
res = subprocess.run(["git", "-C", "agentkit-lead-triage", "diff", "--cached", "--quiet"])
if res.returncode != 0:
    subprocess.run(["git", "-C", "agentkit-lead-triage", "commit", "-m", "Add triage.py with --demo mode and exact scoring"], check=True)
else:
    print("No changes to commit.")
subprocess.run(["git", "-C", "agentkit-lead-triage", "push", "origin", "master"], check=True)
print("Successfully pushed triage.py to GitHub!")
