#!/usr/bin/env python3
"""
Form Guide Parser - Fetches race data from FormFav and exports to Google Sheets.

Usage:
    export GOOGLE_OAUTH_CLIENT_ID=<your_client_id>
    export GOOGLE_OAUTH_CLIENT_SECRET=<your_client_secret>
    python form_guide_to_sheets.py --date 2026-09-30 --tracks balaklava,ballarat,rosehill
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import csv
import io

import requests

# FormFav API configuration
FORMFAV_BASE_URL = "https://api.formfav.com"
FORMFAV_API_KEY = os.environ.get("FORMFAV_API_KEY", "")

if not FORMFAV_API_KEY:
    print("Error: FORMFAV_API_KEY not set in environment", file=sys.stderr)
    sys.exit(1)


def fetch_meetings(date: str, race_code: str = "gallops") -> dict:
    """Fetch race meetings for a given date."""
    url = f"{FORMFAV_BASE_URL}/form/meetings"
    params = {"date": date, "race_code": race_code}
    headers = {"X-API-Key": FORMFAV_API_KEY}
    
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text}")
    return resp.json()


def fetch_race_card(date: str, track: str, race: int, race_code: str = "gallops", country: str = "au") -> dict:
    """Fetch detailed race card."""
    url = f"{FORMFAV_BASE_URL}/form"
    params = {
        "date": date,
        "track": track,
        "race": race,
        "race_code": race_code,
        "country": country
    }
    headers = {"X-API-Key": FORMFAV_API_KEY}
    
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text}")
    return resp.json()


def parse_runners_to_rows(card: dict) -> List[dict]:
    """Parse runner data into flat rows for CSV/Sheets export."""
    rows = []
    for runner in card.get("runners", []):
        rows.append({
            "horseName": runner.get("horseName", ""),
            "barrier": runner.get("barrier", ""),
            "jockeyName": runner.get("jockeyName", ""),
            "weight": runner.get("weight", ""),
            "rating": runner.get("rating", ""),
            "trainerName": runner.get("trainerName", ""),
            "sex": runner.get("sex", ""),
            "age": runner.get("age", ""),
            "color": runner.get("color", ""),
            "form": runner.get("form", ""),
            "last5": runner.get("last5", ""),
            "speedRating": runner.get("speedRating", ""),
            "earnings": runner.get("earnings", ""),
            "runnerId": runner.get("runnerId", ""),
        })
    return rows


def generate_csv_content(rows: List[dict], track: str, race: int, date: str) -> str:
    """Generate CSV content from rows."""
    output = io.StringIO()
    if rows:
        fieldnames = list(rows[0].keys())
        fieldnames.insert(0, "RaceInfo")
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_copy = row.copy()
            row_copy["RaceInfo"] = f"{date}|{track}|Race {race}"
            writer.writerow(row_copy)
    return output.getvalue()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch FormFav race data and export to CSV/Sheets")
    parser.add_argument("--date", required=True, help="Race date (YYYY-MM-DD)")
    parser.add_argument("--tracks", required=True, help="Comma-separated list of track slugs (e.g., balaklava,ballarat)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format")
    parser.add_argument("--all-races", action="store_true", help="Fetch all races for each track")
    
    args = parser.parse_args()
    
    tracks = [t.strip() for t in args.tracks.split(",")]
    
    all_data = {
        "date": args.date,
        "tracks": tracks,
        "races": []
    }
    
    try:
        meetings = fetch_meetings(args.date)
    except Exception as e:
        print(f"Error fetching meetings: {e}", file=sys.stderr)
        sys.exit(1)
    
    for track_slug in tracks:
        # Find the track in meetings
        track_data = None
        for m in meetings.get("meetings", []):
            if m.get("slug") == track_slug and m.get("country") == "au":
                track_data = m
                break
        
        if not track_data:
            print(f"Warning: No meeting found for {track_slug} on {args.date}", file=sys.stderr)
            continue
        
        track_name = track_data.get("track", track_slug)
        races = track_data.get("races", [])
        
        for race_info in races:
            race_num = race_info.get("raceNumber")
            race_name = race_info.get("raceName", f"Race {race_num}")
            
            try:
                card = fetch_race_card(args.date, track_slug, race_num)
                runners = parse_runners_to_rows(card)
                
                race_entry = {
                    "date": args.date,
                    "track": track_name,
                    "track_slug": track_slug,
                    "race_number": race_num,
                    "race_name": race_name,
                    "distance": race_info.get("distance", ""),
                    "condition": race_info.get("condition", ""),
                    "class": race_info.get("raceClass", ""),
                    "runners": runners,
                    "csv_content": generate_csv_content(runners, track_slug, race_num, args.date)
                }
                all_data["races"].append(race_entry)
                print(f"Fetched {track_name} Race {race_num}: {len(runners)} runners", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Error fetching {track_slug} Race {race_num}: {e}", file=sys.stderr)
    
    # Output
    if args.format == "json":
        output = json.dumps(all_data, indent=2)
    else:
        # CSV format - combine all race cards
        csv_parts = []
        for race in all_data.get("races", []):
            if race.get("csv_content"):
                csv_parts.append(race["csv_content"])
        output = "\n".join(csv_parts) if csv_parts else "# No data fetched\n"
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()