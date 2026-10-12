import json
import subprocess
import sys

payload = {
    "fileId": "10h3SBJz7zUfHFZTLd6n_OdDb60d86GCRKMuarXR_d5U",
    "fields": "id,name,mimeType,webViewLink,parents"
}

payload_path = "outputs/gdrive_payload.json"
import pathlib
pathlib.Path(payload_path).parent.mkdir(parents=True, exist_ok=True)
pathlib.Path(payload_path).write_text(json.dumps(payload))

cmd = [
    "composio", "execute", "GOOGLEDRIVE_GET_FILE_METADATA",
    "-d", f"@{payload_path}"
]

print("Verifying Google Drive file metadata via Composio...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)
