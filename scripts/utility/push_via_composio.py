import json
import subprocess
import sys
from pathlib import Path

spreadsheet_id = "1_PAcUXsbiJ6C7h5RUNCLHXBtTpbBCmFNQJ6ddI0jb1I"

# Read MCP_Agents.csv
mcp_csv = Path("outputs/control_centre/MCP_Agents.csv").read_text().splitlines()
mcp_rows = [line.split(",") for line in mcp_csv]

# Read Business_Metrics.csv
metrics_csv = Path("outputs/control_centre/Business_Metrics.csv").read_text().splitlines()
metrics_rows = [line.split(",") for line in metrics_csv]

# Read Product_Inventory.csv
prod_csv = Path("outputs/control_centre/Product_Inventory.csv").read_text().splitlines()
prod_rows = [line.split(",") for line in prod_csv]

all_rows = mcp_rows + [[]] + [["--- BUSINESS METRICS ---"]] + metrics_rows + [[]] + [["--- PRODUCT INVENTORY ---"]] + prod_rows

payload_all = {
    "spreadsheet_id": spreadsheet_id,
    "range": "Sheet1!A1",
    "value_input_option": "USER_ENTERED",
    "values": all_rows
}

cmd_all = ["composio", "execute", "GOOGLESHEETS_VALUES_UPDATE", "-d", json.dumps(payload_all)]
print("Pushing Control Centre data to Google Sheets via Composio...")
result = subprocess.run(cmd_all, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
print("Done!")
