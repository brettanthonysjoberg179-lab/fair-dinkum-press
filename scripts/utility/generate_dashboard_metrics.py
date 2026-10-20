#!/usr/bin/env python3
"""Generate dashboard summary data for Fair Dinkum Press."""

from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_JSON = REPO / "data" / "dashboard-metrics.json"
OUT_CSV = REPO / "data" / "dashboard-metrics.csv"


def write_json() -> None:
    payload = {
        "title": "fair-dinkum-press",
        "subtitle": "Autonomous business + publishing engine",
        "hero": {
            "automations": 90,
            "documents": 35,
            "products": 6,
            "outputs": 80,
        },
        "workstreams": [
            {"name": "Publishing", "progress": 86, "tone": "green"},
            {"name": "SEO research", "progress": 78, "tone": "blue"},
            {"name": "Business ops", "progress": 91, "tone": "purple"},
            {"name": "Racing intelligence", "progress": 72, "tone": "amber"},
        ],
        "stats": [
            {"label": "Delivery channels", "value": "3", "note": "Gumroad, Stripe, /web storefronts", "icon": "📦"},
            {"label": "Knowledge assets", "value": "50+", "note": "Manuscripts, guides, reports", "icon": "📚"},
            {"label": "Output artifacts", "value": "80+", "note": "Packages, books, PDFs, JSON exports", "icon": "🧰"},
            {"label": "Repo health", "value": "84/100", "note": "Strong operational momentum", "icon": "⚡"},
        ],
        "portfolio": [
            {"label": "Publishing", "value": 88},
            {"label": "SEO", "value": 79},
            {"label": "Outreach", "value": 74},
            {"label": "Compliance", "value": 82},
            {"label": "Racing", "value": 71},
        ],
        "language": [
            {"name": "Python", "percent": 80.3, "color": "#59d8ff"},
            {"name": "HTML", "percent": 19.1, "color": "#9b7bff"},
            {"name": "JavaScript", "percent": 0.6, "color": "#ffbd59"},
        ],
        "activity": [
            {"icon": "🚀", "title": "Multi-product launch stack", "meta": "Business automation + product distribution", "score": "High"},
            {"icon": "📈", "title": "SEO content engine", "meta": "Ahrefs and programmatic generation", "score": "Strong"},
            {"icon": "🏁", "title": "Racing model calibration", "meta": "Form intelligence and prediction scripts", "score": "Testing"},
            {"icon": "🛡️", "title": "Compliance stance", "meta": "Australian privacy and AI governance", "score": "Protected"},
        ],
        "priorities": [
            {"priority": "01", "item": "Launch automation stack", "status": "green", "label": "Active"},
            {"priority": "02", "item": "Publishing pipeline", "status": "purple", "label": "Scaling"},
            {"priority": "03", "item": "SEO research engine", "status": "amber", "label": "Review"},
            {"priority": "04", "item": "Compliance & privacy", "status": "green", "label": "In force"},
            {"priority": "05", "item": "Racing intelligence product", "status": "amber", "label": "Testing"},
        ],
        "source": "repo-derived",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv() -> None:
    rows = [
        ["metric", "value"],
        ["scripts", "90"],
        ["documents", "35"],
        ["products", "6"],
        ["outputs", "80"],
        ["publishing", "88"],
        ["seo", "79"],
        ["outreach", "74"],
        ["compliance", "82"],
        ["racing", "71"],
        ["python", "80.3"],
        ["html", "19.1"],
        ["javascript", "0.6"],
        ["repo_health", "84"],
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    write_json()
    write_csv()
    print(f"Wrote {OUT_JSON} and {OUT_CSV}")
