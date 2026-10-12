#!/usr/bin/env python3
"""Generate AI-Powered Content & Compliance Machine PDF guide."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, HRFlowable, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

OUTPUT_PATH = "/home/brettanthonysjoberg179/ai-content-compliance-machine.pdf"

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
        self.drawString(54, 11 * inch - 36, "AI-Powered Content & Compliance Machine — Notion OS Guide")
        self.setStrokeColor(HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — FAIR DINKUM DIGITAL PRODUCTS")
        self.line(54, 48, 8.5 * inch - 54, 48)
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=HexColor('#0F172A'),
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=20,
        textColor=HexColor('#475569'),
        alignment=TA_LEFT
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=HexColor('#0F172A'),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=HexColor('#1E293B'),
        spaceBefore=14,
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
        spaceBefore=4,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=13,
        textColor=HexColor('#0F172A')
    )

    story = []
    
    # --- COVER PAGE ---
    story.append(Spacer(1, 40))
    story.append(Paragraph("FAIR DINKUM DIGITAL PRODUCTS", ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=HexColor('#2563EB'))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("AI-Powered Content & Compliance Machine", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("The Complete Notion OS & AI Prompt Workspace for Local Businesses, Trades, and Professional Services", subtitle_style))
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=3, color=HexColor('#2563EB'), spaceBefore=0, spaceAfter=25))
    
    # Metadata Box
    meta_data = [
        [Paragraph("<b>Version:</b> 2026.1", body_style), Paragraph("<b>Author:</b> Fair Dinkum Research Group", body_style)],
        [Paragraph("<b>Target Audience:</b> Local Business & Trades", body_style), Paragraph("<b>Included:</b> Notion Dashboard + 100+ AI Prompts", body_style)]
    ]
    t = Table(meta_data, colWidths=[200, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 40))
    
    # Executive Summary Box
    exec_summary = "<b>Executive Summary:</b> In 2026, local service businesses and trades face intense local competition. This comprehensive Notion OS and AI prompt workspace bridges the gap, providing plug-and-play client acquisition systems, automated social media planning, and bulletproof compliance checklists designed specifically for non-technical operators."
    story.append(Table([[Paragraph(exec_summary, body_style)]], colWidths=[450], style=[
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#BFDBFE')),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    
    story.append(PageBreak())
    
    # --- TABLE OF CONTENTS ---
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=15))
    
    toc_data = [
        [Paragraph("<b>1. Introduction: AI & Notion OS for Local Businesses</b>", body_style), Paragraph("<b>Page 3</b>", body_style)],
        [Paragraph("<b>2. The Content Machine: 100+ Pre-Tested AI Prompts</b>", body_style), Paragraph("<b>Page 5</b>", body_style)],
        [Paragraph("<b>3. Social Media Calendar & Auto-Scheduling Workflow</b>", body_style), Paragraph("<b>Page 8</b>", body_style)],
        [Paragraph("<b>4. Local Business Compliance Checklist & Regulatory Frameworks</b>", body_style), Paragraph("<b>Page 11</b>", body_style)],
        [Paragraph("<b>5. Implementation & Setup Guide</b>", body_style), Paragraph("<b>Page 14</b>", body_style)],
    ]
    t_toc = Table(toc_data, colWidths=[360, 90])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_toc)
    
    story.append(PageBreak())
    
    # --- SECTION 1 ---
    story.append(Paragraph("1. Introduction: AI & Notion OS for Local Businesses", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("Local business owners—plumbers, electricians, landscapers, consultants, and real estate professionals—routinely lose 15–20 hours a week to administrative overhead, content creation, and compliance tracking. While enterprise businesses deploy expensive AI software, solo operators and small teams often lack the time or technical know-how to harness artificial intelligence effectively.", body_style))
    story.append(Paragraph("The <b>AI-Powered Content & Compliance Machine</b> solves this problem by embedding pre-tested, high-converting prompts and automated workflows directly into a customized Notion workspace. You don't need to learn prompt engineering or complex automation platforms; you simply duplicate the template and start generating client proposals, social media posts, and compliance audits in seconds.", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Core Architecture of the System", h2_style))
    story.append(Paragraph("Our Notion OS is built on four interconnected pillars:", body_style))
    story.append(Paragraph("• <b>Pillar 1: Client Acquisition Engine</b> — Instant proposal generators, cold email outreach sequences, and follow-up templates.", body_style))
    story.append(Paragraph("• <b>Pillar 2: Social Media Content Factory</b> — Weekly content calendars, hook libraries, and platform-specific repurposing guides.", body_style))
    story.append(Paragraph("• <b>Pillar 3: Regulatory Compliance Vault</b> — Essential checklists for licensing, insurance, safety protocols, and data privacy.", body_style))
    story.append(Paragraph("• <b>Pillar 4: AI Prompt Command Center</b> — 100+ copy-paste prompts optimized for ChatGPT (GPT-4o) and Claude 3.5 Sonnet.", body_style))

    story.append(PageBreak())
    
    # --- SECTION 2 ---
    story.append(Paragraph("2. The Content Machine: 100+ Pre-Tested AI Prompts", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("Generic AI prompts yield generic, unusable results. To get high-converting marketing copy and professional client communications, prompts require strict persona constraints, tone guidelines, and structured output formats. Below are core sample prompts included in the Notion workspace.", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Prompt Template 1: High-Converting Local Service Proposal", h2_style))
    story.append(Paragraph("Use this prompt to generate professional, persuasive project proposals in under 60 seconds.", body_style))
    
    sample_prompt = """Act as an expert commercial copywriter and estimator for local trades and services.
Write a professional, persuasive project proposal for [Client Name] regarding [Project Type].
Project Scope: [Insert Scope Details]
Pricing Structure: [Insert Pricing / Fixed or Hourly]
Timeline: [Insert Duration]

Requirements:
1. Emphasize reliability, licensing, and insurance.
2. Outline clear milestones and payment terms.
3. Include a polite call-to-action for signing within 48 hours."""
    
    story.append(Spacer(1, 4))
    story.append(Table([[Paragraph(sample_prompt.replace('\n', '<br/>'), code_style)]], colWidths=[450], style=[
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Prompt Template 2: Local SEO Google Business Profile Post", h2_style))
    story.append(Paragraph("Drive local search traffic with optimized weekly updates.", body_style))
    story.append(Spacer(1, 4))
    
    sample_prompt_2 = """Act as a local SEO specialist. Write a Google Business Profile update for [Business Name] located in [City/Region].
Service Highlight: [Service Name e.g., Emergency Plumbing]
Customer Benefit: [Benefit e.g., 24/7 fast response, upfront pricing]
Call-to-Action: Call [Phone Number] or book online at [URL].

Constraints: Keep under 150 words. Include 3 relevant local hashtags."""
    
    story.append(Table([[Paragraph(sample_prompt_2.replace('\n', '<br/>'), code_style)]], colWidths=[450], style=[
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))

    story.append(PageBreak())
    
    # --- SECTION 3 ---
    story.append(Paragraph("3. Social Media Calendar & Auto-Scheduling Workflow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("Consistency is the #1 driver of organic social media growth for local businesses. The Notion Content Calendar included in this package provides a 4-week rotating content matrix designed to educate, build trust, and drive inbound inquiries.", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Weekly Content Matrix Structure", h2_style))
    
    matrix_data = [
        [Paragraph("<b>Day</b>", body_style), Paragraph("<b>Content Pillar</b>", body_style), Paragraph("<b>Format</b>", body_style)],
        [Paragraph("Monday", body_style), Paragraph("Educational / 'How It Works'", body_style), Paragraph("Carousel / Short Video", body_style)],
        [Paragraph("Tuesday", body_style), Paragraph("Client Case Study / Before-After", body_style), Paragraph("Photo / Testimonial", body_style)],
        [Paragraph("Wednesday", body_style), Paragraph("Behind-the-Scenes / Team Spotlight", body_style), Paragraph("Reel / Story", body_style)],
        [Paragraph("Thursday", body_style), Paragraph("Myth-Busting / Industry Tip", body_style), Paragraph("Text Post / Graphic", body_style)],
        [Paragraph("Friday", body_style), Paragraph("Direct Offer / Weekend Availability", body_style), Paragraph("Promotional Post", body_style)],
    ]
    t_matrix = Table(matrix_data, colWidths=[90, 210, 150])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor('#FFFFFF')),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_matrix)

    story.append(PageBreak())
    
    # --- SECTION 4 ---
    story.append(Paragraph("4. Regulatory Compliance Checklist & Frameworks", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("Operating without rigorous compliance documentation exposes local businesses to severe liability. The compliance vault provides audit-ready templates for insurance verification, worker safety briefings, and customer data protection.", body_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Core Compliance Modules Included", h2_style))
    story.append(Paragraph("1. <b>Licensing & Accreditation Tracker</b>: Automated renewal alerts and credential verification logs.", body_style))
    story.append(Paragraph("2. <b>Job Site Safety Briefing SOP</b>: Standardized pre-work safety checklist for field workers.", body_style))
    story.append(Paragraph("3. <b>Customer Privacy & Data Policy</b>: GDPR and consumer privacy compliant data collection templates.", body_style))
    story.append(Paragraph("4. <b>Subcontractor Agreement Templates</b>: Bulletproof indemnity clauses and scope definitions.", body_style))

    story.append(PageBreak())
    
    # --- SECTION 5 ---
    story.append(Paragraph("5. Implementation & Setup Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("Getting started takes less than 5 minutes. Follow these simple steps to deploy your Notion OS and AI Prompt Workspace:", body_style))
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Step 1: Duplicate the Notion Template</b>", h2_style))
    story.append(Paragraph("Click the secure access link provided in your purchase confirmation email. Once open in your Notion account, click 'Duplicate' in the top right corner to save a private copy to your workspace.", body_style))
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Step 2: Customize Your Business Profile</b>", h2_style))
    story.append(Paragraph("Navigate to the 'Settings & Profile' database inside the template. Input your business name, service categories, pricing rates, and brand voice preferences so the AI prompts auto-fill correctly.", body_style))
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Step 3: Pin Your Favorite AI Prompts</b>", h2_style))
    story.append(Paragraph("Open the 'Prompt Library' database, filter by your current focus (e.g., Proposals, Social Media, Email Outreach), and begin generating copy instantly with ChatGPT or Claude.", body_style))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#CBD5E1'), spaceBefore=10, spaceAfter=10))
    story.append(Paragraph("<b>Thank you for choosing Fair Dinkum Digital Products.</b> For support, updates, or custom enterprise deployments, reach out to our team at support@fairdinkum.digital.", ParagraphStyle('FooterNote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, textColor=HexColor('#64748B'), alignment=TA_CENTER)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
