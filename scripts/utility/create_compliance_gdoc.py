import json
import subprocess
import pathlib
import sys

# Read AI compliance launch packet markdown
md_path = "AI_COMPLIANCE_LAUNCH_PACKET.md"
content = pathlib.Path(md_path).read_text(encoding="utf-8")

# Prepare title and markdown text
title = "The AU AI Compliance Playbook - Launch & Outreach Packet (Fair Dinkum)"

payload = {
    "title": title,
    "markdown_text": content,
    "image_assets": []
}

payload_path = "outputs/compliance_gdoc_payload.json"
pathlib.Path(payload_path).parent.mkdir(parents=True, exist_ok=True)
pathlib.Path(payload_path).write_text(json.dumps(payload, indent=2))

print(f"Payload prepared with {len(content)} characters. Executing Composio tool GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN...")

cmd = [
    "composio", "execute", "GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN",
    "-d", f"@{payload_path}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
if res.stderr:
    print("STDERR:", file=sys.stderr)
    print(res.stderr, file=sys.stderr)

if res.returncode == 0:
    # Save output log
    pathlib.Path("outputs/compliance_gdoc_result.json").write_text(res.stdout)
    print("Successfully created Google Doc!")
else:
    print(f"Command failed with exit code {res.returncode}", file=sys.stderr)
    sys.exit(res.returncode)
