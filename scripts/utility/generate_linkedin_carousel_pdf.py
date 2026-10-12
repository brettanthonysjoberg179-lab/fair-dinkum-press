from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "outputs/fair_dinkum_book_catalog_carousel.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter),
                        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'SlideTitle',
    parent=styles['Heading1'],
    fontSize=26,
    leading=32,
    textColor=colors.HexColor('#111827'),
    spaceAfter=12
)

subtitle_style = ParagraphStyle(
    'SlideSubtitle',
    parent=styles['Normal'],
    fontSize=16,
    leading=22,
    textColor=colors.HexColor('#f59e0b'),
    spaceAfter=16,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'SlideBody',
    parent=styles['Normal'],
    fontSize=14,
    leading=20,
    textColor=colors.HexColor('#374151'),
    spaceAfter=14
)

footer_style = ParagraphStyle(
    'SlideFooter',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#9ca3af')
)

products = [
    ("Fair Dinkum Publishing & AI Advisory", "Autonomous Solopreneur & Digital Product Catalog", "Edge-native playbooks, AI compliance frameworks, and high-margin digital assets for modern creators.", "Catalog 2026 Edition"),
    ("The AU AI Compliance Playbook", "Tier 3 / Regulatory Playbook — A$147 AUD", "Essential guidance and privacy policy templates for Australian fintechs, lenders, and e-commerce navigating Privacy Act APP 1.7.", "✓ 207-Page Guide | 90-Day Checklist | Policy Templates"),
    ("AU AI Compliance Readiness Report", "Tier 5 / Advisory Audit — A$149 AUD", "Done-for-you automated regulatory scan, custom risk assessment report, and 1-on-1 strategy session.", "✓ Automated Stack Scan | Custom PDF Report | 1-on-1 Strategy"),
    ("Automated Book Writer & Workforce", "Enterprise Tier / SaaS — A$99 / month", "Deploy a fully autonomous multi-agent workforce that researches, writes, formats, and publishes professional books.", "✓ Multi-Agent Orchestration | RAG Memory | Auto-Publishing"),
    ("Aussie Agent Workflowz Playbook", "Tier 2 / Workflow Toolkit — A$49 AUD", "Battle-tested Python and Composio agent workflows designed for Australian businesses to automate support and outreach.", "✓ Composio Agents | ClickSend SMS | Cloudflare Workers"),
    ("Skate + Graffiti 2-Pack Bundle", "Special Bundle — A$45 AUD", "The ultimate cultural history bundle pairing two comprehensive design and subculture books at a 22% discount.", "✓ History of Skateboarding (114pp) | History of Graffiti (120pp)"),
    ("CC0 Sample Library Curation", "Creator Tier / Asset Pack — A$40 AUD", "Curated archive of high-fidelity public domain audio samples, textures, and visual assets for commercial digital production.", "✓ 100% CC0 Royalty-Free | Master Audio Stems & Textures"),
    ("The History of Graffiti", "Tier 1 / Cultural History — A$29 AUD", "From subway cars in 1970s New York to global contemporary galleries—explore typography, rebellion, and street art.", "✓ 120-Page Illustrated Guide | Eras, Styles & Typography"),
    ("The History of Skateboarding", "Tier 1 / Cultural History — A$29 AUD", "From clay wheels and sidewalk surfing in the 1950s to Dogtown pioneers, the Bones Brigade, and Tokyo 2020.", "✓ 114-Page Comprehensive Book | 18 Historical Eras"),
    ("Solopreneur OS", "Tier 1 / Productivity Playbook — A$29 AUD", "The definitive operational system and framework for solo founders to automate admin, scale products, and run a lean business.", "✓ Operational Frameworks | Notion Templates | Automation Ledger"),
    ("AI Side Hustle Toolkit", "Tier 1 / Micro-Toolkit — A$9.90 AUD", "50 battle-tested AI prompts, geo-keyword checklists, and automation templates to launch a profitable side hustle in 48 hours.", "✓ 50 Pro-Tested Prompts | Local SEO Checklist | Quick-Start Guide")
]

story = []
total = len(products)

for idx, (title, subtitle, desc, details) in enumerate(products, 1):
    story.append(Paragraph(f"<b>{title}</b>", title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(desc, body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Key Highlights:</b><br/>{details}", body_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"Fair Dinkum Publishing & AI Advisory | Slide {idx} of {total}", footer_style))
    if idx < total:
        story.append(PageBreak())

doc.build(story)
print(f"Successfully generated LinkedIn PDF carousel at {pdf_path}")
