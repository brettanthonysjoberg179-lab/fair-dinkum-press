#!/usr/bin/env python3
"""Generate Fair Dinkum Business Operations Manual PDF booklet and email it."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
import os
import json
import subprocess
import sys

PDF_PATH = "outputs/fair_dinkum_business_operations_manual.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(HexColor("#64748B"))
        
        # Header
        self.drawString(54, 11 * inch - 36, "Fair Dinkum Publishing — Business Operations Manual")
        self.setStrokeColor(HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — FAIR DINKUM PUBLISHING")
        self.line(54, 48, 8.5 * inch - 54, 48)
        
        self.restoreState()

def build_pdf():
    os.makedirs("outputs", exist_ok=True)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=HexColor('#475569')
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=HexColor('#0F172A'),
        spaceBefore=16,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=HexColor('#334155'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=HexColor('#334155')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=HexColor('#FFFFFF')
    )

    story = []

    # --- COVER PAGE ---
    story.append(Spacer(1, 40))
    story.append(Paragraph("FAIR DINKUM PUBLISHING & AI ADVISORY", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Master Business Operations Manual & Autonomous Agent Architecture", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=3, color=HexColor('#0F172A'), spaceAfter=20, spaceBefore=0))
    
    story.append(Paragraph("<b>Effective Date:</b> October 9, 2026", body_style))
    story.append(Paragraph("<b>Status:</b> Operational / Production-Ready", body_style))
    story.append(Paragraph("<b>Founder & Managing Director:</b> Brett Sjoberg", body_style))
    story.append(Paragraph("<b>Jurisdiction:</b> Australia (Federal Privacy Act 1988, Corporations Act 2001)", body_style))
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("<b>Executive Summary:</b><br/>This operational manual defines the corporate structure, product value ladder, Cloudflare edge infrastructure, and autonomous agentic workflows (Composio, Python, ClickSend SMS) powering Fair Dinkum Publishing & AI Advisory.", body_style))
    story.append(PageBreak())

    # --- SECTION 1 ---
    story.append(Paragraph("1. Executive Corporate Structure & Governance", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceAfter=10, spaceBefore=2))
    story.append(Paragraph("<b>1.1 Mission Statement</b><br/>Fair Dinkum Publishing & AI Advisory delivers frictionless, edge-native digital publishing and B2B artificial intelligence compliance advisory. We bridge the gap between complex regulatory mandates (specifically the Australian Privacy Act 1988 and APP 1.7 Automated Decision-Making disclosures) and modern autonomous AI business operations.", body_style))
    story.append(Paragraph("<b>1.2 Legal & Tax Compliance Framework</b><br/>• <b>Entity Type:</b> Australian Sole Trader / Proprietary Limited (Pty Ltd) holding Australian Business Number (ABN) and Business Name registration.<br/>• <b>Taxation:</b> Goods and Services Tax (GST) registered where turnover exceeds threshold; digital products taxed under standard Australian digital service rules.<br/>• <b>Privacy & Compliance Rails:</b><br/>  - <b>APP 1.7 Compliance:</b> Every automated decision-making system operated by Fair Dinkum or its clients maintains transparent public disclosure registers.<br/>  - <b>Data Sovereignty:</b> Customer data, SQLite D1 ledgers, and R2 assets are stored securely within Cloudflare's Australian/Global edge network under strict data protection protocols.", bullet_style))

    # --- SECTION 2 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Product Catalog & Value Ladder", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceAfter=10, spaceBefore=2))
    story.append(Paragraph("Fair Dinkum operates a high-margin, scalable digital product value ladder paired with high-ticket advisory:", body_style))
    
    table_data = [
        [Paragraph("Tier", table_header_style), Paragraph("Product Name", table_header_style), Paragraph("Price (AUD)", table_header_style), Paragraph("Format / Delivery", table_header_style)],
        [Paragraph("Tier 1", table_cell_style), Paragraph("Geo-Keyword & Prompt Toolkit", table_cell_style), Paragraph("$29 – $49", table_cell_style), Paragraph("PDF / EPUB / ZIP via R2", table_cell_style)],
        [Paragraph("Tier 2", table_cell_style), Paragraph("FOUND ON AI", table_cell_style), Paragraph("$97", table_cell_style), Paragraph("Book + 5 Agent Workflows", table_cell_style)],
        [Paragraph("Tier 3", table_cell_style), Paragraph("AU AI Compliance Playbook", table_cell_style), Paragraph("$149", table_cell_style), Paragraph("Compliance Pkg + Templates", table_cell_style)],
        [Paragraph("Tier 4", table_cell_style), Paragraph("Autonomous Solopreneur Bundle", table_cell_style), Paragraph("$297", table_cell_style), Paragraph("Complete Asset Inventory", table_cell_style)],
        [Paragraph("Tier 5", table_cell_style), Paragraph("DFY AI Compliance Audit", table_cell_style), Paragraph("$1,500", table_cell_style), Paragraph("Custom PDF Audit Report", table_cell_style)],
    ]
    t = Table(table_data, colWidths=[40, 150, 70, 244])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#F8FAFC')),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # --- SECTION 3 ---
    story.append(Paragraph("3. Cloudflare Edge Architecture & Infrastructure", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceAfter=10, spaceBefore=2))
    story.append(Paragraph("Fair Dinkum operates a zero-maintenance, serverless edge infrastructure hosted on Cloudflare:", body_style))
    story.append(Paragraph("• <b>Cloudflare Workers:</b> Edge compute handling Stripe & Gumroad webhook events instantly at sub-50ms latency.<br/>• <b>Cloudflare R2 Storage:</b> Secure object storage for heavy EPUBs, ZIP packages, and book covers with zero egress fees and automated 7-day signed download URL generation.<br/>• <b>Cloudflare D1 / KV:</b> Edge SQLite database tracking B2B regulatory prospects and transactional ledgers.<br/>• <b>Cloudflare Access (Zero Trust):</b> Secures internal agent control centres behind Email OTP and GitHub OAuth.", bullet_style))

    # --- SECTION 4 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Autonomous Agentic Workforce & Tooling Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceAfter=10, spaceBefore=2))
    story.append(Paragraph("Fair Dinkum deploys an autonomous agentic workforce powered by Composio, Python, and LLM backends:", body_style))
    
    agent_data = [
        [Paragraph("Agent Name", table_header_style), Paragraph("Operational Domain", table_header_style), Paragraph("Connected Toolkits", table_header_style), Paragraph("Trigger", table_header_style)],
        [Paragraph("Outreach Growth", table_cell_style), Paragraph("B2B lead generation", table_cell_style), Paragraph("Gmail, D1 SQLite", table_cell_style), Paragraph("Daily Cron", table_cell_style)],
        [Paragraph("Inbox Listener", table_cell_style), Paragraph("Inbound inquiry processing", table_cell_style), Paragraph("Gmail, Calendar", table_cell_style), Paragraph("Webhook", table_cell_style)],
        [Paragraph("SMS Review", table_cell_style), Paragraph("Post-job review requests", table_cell_style), Paragraph("ClickSend SMS", table_cell_style), Paragraph("1 Hr Post-Job", table_cell_style)],
        [Paragraph("Financial Ledger", table_cell_style), Paragraph("Revenue tracking & invoicing", table_cell_style), Paragraph("Airtable, Sheets", table_cell_style), Paragraph("End of Day", table_cell_style)],
    ]
    t2 = Table(agent_data, colWidths=[90, 130, 130, 154])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#F8FAFC')),
    ]))
    story.append(t2)

    # --- SECTION 5 & 6 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Standard Operating Procedures (SOPs)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceAfter=10, spaceBefore=2))
    story.append(Paragraph("• <b>SOP-001 (Publishing):</b> Draft Markdown manuscript -> Generate cover -> Run `package_for_gumroad.py` -> Upload ZIP to R2 -> Publish SKU.<br/>• <b>SOP-002 (B2B Outreach):</b> Generate programmatic leads -> Audit compliance -> Dispatch personalized email via Composio Gmail agent -> Follow up via ClickSend SMS.<br/>• <b>SOP-003 (Fulfillment & Review):</b> Stripe/Gumroad webhook -> Instant R2 signed URL delivery -> Automated review SMS dispatch (`CLICKSEND_CREATE_SMS_SEND`).", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF booklet at {PDF_PATH}")

if __name__ == '__main__':
    build_pdf()
