#!/usr/bin/env python3
"""
AgentKit & Ebook Portfolio Presentation Generator
================================================
Generates a professional PowerPoint presentation (.pptx) ready for Google Slides import,
featuring all Ebooks, the 5-workflow AgentKit pack, and direct Stripe checkout links.

Usage:
    python generate_ebook_slides.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank slide
    
    # Color palette
    BG_DARK = RGBColor(15, 23, 42)      # #0f172a
    CARD_BG = RGBColor(30, 41, 59)      # #1e293b
    TEXT_LIGHT = RGBColor(248, 250, 252) # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184) # #94a3b8
    ACCENT_BLUE = RGBColor(56, 189, 248) # #38bdf8
    ACCENT_GREEN = RGBColor(34, 197, 94) # #22c55e

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # ==================== SLIDE 1: Title Slide ====================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, BG_DARK)
    
    # Title Box
    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "🤖 The Autonomous Solopreneur & AgentKit Library"
    p0.font.size = Pt(40)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE
    p0.space_after = Pt(20)
    
    p1 = tf.add_paragraph()
    p1.text = "Production-Ready AI Agent Workflows, Ebooks & Digital Asset Portfolio"
    p1.font.size = Pt(24)
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(30)
    
    p2 = tf.add_paragraph()
    p2.text = "Instant Access • Powered by Python, Composio & Stripe"
    p2.font.size = Pt(16)
    p2.font.color.rgb = ACCENT_GREEN

    # ==================== SLIDE 2: Digital Asset Portfolio ====================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_DARK)
    
    tb2 = slide2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📚 Digital Asset Portfolio Overview"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    content2 = [
        ("The Autonomous Solopreneur (Ebook & Workbook)", "Comprehensive guides on building, scaling, and automating a solo digital business to $10K+/month."),
        ("Programmatic SEO Dominance", "Complete blueprints for automated programmatic content generation, SEO rankings, and traffic engines."),
        ("AgentKit Small Business Automation Pack", "Production-ready Python workflow templates for lead triage, invoice chasing, and CRM sync.")
    ]
    
    top_pos = Inches(2.2)
    for title, desc in content2:
        box = slide2.shapes.add_textbox(Inches(1.0), top_pos, Inches(11.333), Inches(1.2))
        tf = box.text_frame
        tf.word_wrap = True
        p_title = tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT
        p_title.space_after = Pt(6)
        
        p_desc = tf.add_paragraph()
        p_desc.text = f"   {desc}"
        p_desc.font.size = Pt(16)
        p_desc.font.color.rgb = TEXT_MUTED
        top_pos += Inches(1.5)

    # ==================== SLIDE 3: AgentKit 5-Workflow Pack ====================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_DARK)
    
    tb3 = slide3.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚙️ AgentKit Shop: 5-Workflow Automation Pack"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    workflows = [
        "1. Inbound Lead Triage & Gmail Reply Draft Agent (Auto-scores Hot/Warm/Cold leads)",
        "2. Overdue Invoice Chaser Agent (Sends polite reminders with instant Stripe links)",
        "3. Lead Enrichment & CRM Sync Agent (Enriches company data & syncs to Google Sheets)",
        "4. Automated Follow-up Sequencer Agent (Multi-step outreach automation)",
        "5. Meeting Scheduler & Calendar Booker Agent (Parses invite requests via Composio)"
    ]
    
    top_pos = Inches(2.0)
    for wf in workflows:
        box = slide3.shapes.add_textbox(Inches(1.0), top_pos, Inches(11.333), Inches(0.8))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = wf
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_LIGHT
        top_pos += Inches(0.9)

    # ==================== SLIDE 4: Pricing & Stripe Links ====================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_DARK)
    
    tb4 = slide4.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "🛒 Pricing & Instant Stripe Checkout"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    pricing_info = [
        ("AgentKit Small Business Pack (All 5 Workflows)", "$19 USD", "https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u"),
        ("The Autonomous Solopreneur Ebook & Workbook", "$29 USD", "https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u"),
        ("All-Access Masterclass & Asset Bundle", "$149 USD", "https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u")
    ]

    top_pos = Inches(2.2)
    for item, price, link in pricing_info:
        box = slide4.shapes.add_textbox(Inches(1.0), top_pos, Inches(11.333), Inches(1.2))
        tf = box.text_frame
        tf.word_wrap = True
        p_item = tf.paragraphs[0]
        p_item.text = f"• {item} — {price}"
        p_item.font.size = Pt(20)
        p_item.font.bold = True
        p_item.font.color.rgb = ACCENT_GREEN
        p_item.space_after = Pt(6)
        
        p_link = tf.add_paragraph()
        p_link.text = f"   Instant Checkout: {link}"
        p_link.font.size = Pt(14)
        p_link.font.color.rgb = ACCENT_BLUE
        top_pos += Inches(1.5)

    # ==================== SLIDE 5: Call to Action ====================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_DARK)
    
    tb5 = slide5.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.5))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    
    p0 = tf5.paragraphs[0]
    p0.text = "🚀 Accelerate Your Automation Stack Today"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE
    p0.space_after = Pt(20)
    
    p1 = tf5.add_paragraph()
    p1.text = "Get instant download access, private GitHub repository collaboration, and automated onboarding."
    p1.font.size = Pt(20)
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_after = Pt(30)
    
    p2 = tf5.add_paragraph()
    p2.text = "Secure Checkout: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_GREEN

    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "AgentKit_and_Ebooks_Presentation.pptx"
    prs.save(output_path)
    print(f"✅ Presentation saved successfully: {output_path}")

if __name__ == "__main__":
    create_presentation()
