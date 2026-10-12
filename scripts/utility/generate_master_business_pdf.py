#!/usr/bin/env python3
"""Generate Fair Dinkum Master Business Profile PDF booklet."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
import os

OUTPUT_PATH = "outputs/fair_dinkum_master_business_profile.pdf"

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
        self.drawString(54, 11 * inch - 36, "Fair Dinkum Publishing & AI Advisory — Master Business Profile")
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
        OUTPUT_PATH,
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
        fontSize=13,
        leading=18,
        textColor=HexColor('#475569')
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=HexColor('#0F172A'),
        spaceBefore=16,
        spaceAfter=6,
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
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=HexColor('#334155'),
        leftIndent=15,
        spaceAfter=4
    )

    story = []
    
    # Cover Page
    story.append(Spacer(1, 100))
    story.append(Paragraph("🇦🇺 Fair Dinkum Publishing & AI Advisory", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Master Business Profile & Cloudflare Edge Architecture", subtitle_style))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=3, color=HexColor("#2563EB"), spaceAfter=30))
    story.append(Paragraph("<b>Author:</b> Brett Sjoberg", body_style))
    story.append(Paragraph("<b>Date:</b> October 7, 2026", body_style))
    story.append(Paragraph("<b>Status:</b> Live, Autonomous & Cloudflare-Integrated", body_style))
    story.append(PageBreak())
    
    # Section 1
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph(
        "Fair Dinkum Publishing & AI Advisory is an autonomous digital publishing and B2B AI consulting enterprise based in Australia. "
        "The business bridges high-value regulatory compliance advisory (specifically targeting the Australian Privacy Act 1988 and APP 1.7 "
        "Automated Decision-Making disclosure mandates) with automated digital product publishing, programmatic SEO traffic generation, "
        "and edge-native cloud infrastructure.",
        body_style
    ))
    
    # Section 2
    story.append(Paragraph("2. Product & Offer Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("The business operates a tiered value ladder designed for high conversion and lifetime customer value:", body_style))
    story.append(Paragraph("• <b>Micro-Digital Products ($29 – $97):</b> FOUND ON AI ($97) & 5 Niche AI Agent Workflows ($97), Geo-Toolkit templates.", bullet_style))
    story.append(Paragraph("• <b>Mid-Ticket Core Playbooks ($149):</b> The AU AI Compliance Playbook (Privacy Act 1988 + APP 1.7 ADM disclosure gaps).", bullet_style))
    story.append(Paragraph("• <b>High-Ticket Empire Super-Bundle ($297):</b> Complete asset inventory bundle, e-books, EPUBs, workbook covers, and deployable automation scripts.", bullet_style))
    story.append(Paragraph("• <b>High-Ticket Consulting & Advisory ($1,500):</b> Done-For-You (DFY) AI Compliance Audit & Report services delivered via automated compliance scanner agents.", bullet_style))
    
    # Section 3
    story.append(Paragraph("3. Technology & Automation Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("• <b>Core Runtime:</b> Python, Node.js, FastAPI, Next.js.", bullet_style))
    story.append(Paragraph("• <b>Agentic Workflows:</b> Composio-backed background agents (email_trigger_agent.py, composio_outreach_agent.py) handling inbound sales and lead generation.", bullet_style))
    story.append(Paragraph("• <b>Traffic & SEO:</b> Programmatic SEO generator targeting regional B2B fintech and lending markets across Australia.", bullet_style))

    # Section 4
    story.append(Paragraph("4. Cloudflare Edge Architecture & Integration", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("• <b>Cloudflare R2 Storage:</b> Hosts digital product packages (ZIPs, EPUBs) with zero egress fees, generating 7-day signed download URLs for customer fulfillment.", bullet_style))
    story.append(Paragraph("• <b>Cloudflare Workers & Pages:</b> Edge-native API processing Stripe and Gumroad webhooks instantly, logging transactions into Cloudflare D1.", bullet_style))
    story.append(Paragraph("• <b>Cloudflare D1 Database:</b> Distributed SQLite database storing B2B regulatory prospects (Jacaranda Finance, Money3, Hume Bank, SocietyOne).", bullet_style))
    story.append(Paragraph("• <b>Cloudflare Access (Zero Trust):</b> Secures internal agent control centers and financial ledgers behind Email OTP / OAuth authentication.", bullet_style))

    # Section 5
    story.append(Paragraph("5. Growth & Acquisition Flywheel", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#CBD5E1"), spaceAfter=10))
    story.append(Paragraph("1. <b>Programmatic Lead Gen:</b> Scrapes and targets Australian entities with regulatory compliance gaps (APP 1.7 ADM).", bullet_style))
    story.append(Paragraph("2. <b>Automated Outreach:</b> Composio email agents nurture prospects with tailored audit reports.", bullet_style))
    story.append(Paragraph("3. <b>Edge E-Commerce:</b> Gumroad & Stripe checkouts trigger instant edge fulfillment via Cloudflare Workers & R2.", bullet_style))
    story.append(Paragraph("4. <b>Upsell & Retention:</b> Automated cross-sell sequences convert low-ticket buyers into $1,500 DFY compliance audit clients.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
