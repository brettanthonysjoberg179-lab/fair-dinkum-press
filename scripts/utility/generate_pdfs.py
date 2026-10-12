#!/usr/bin/env python3
"""Generate professional PDFs for Gumroad products using reportlab."""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

PRIMARY = HexColor('#2563eb')
ACCENT = HexColor('#7c3aed')
DARK = HexColor('#1e293b')
LIGHT = HexColor('#f8fafc')
GRAY = HexColor('#64748b')

def build_styles():
    styles = getSampleStyleSheet()
    title = ParagraphStyle('Title2', parent=styles['Title'], fontSize=32, leading=38, textColor=PRIMARY, spaceAfter=20, fontName='Helvetica-Bold')
    subtitle = ParagraphStyle('Subtitle2', parent=styles['Normal'], fontSize=14, leading=20, textColor=GRAY, spaceAfter=40, alignment=TA_CENTER)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=22, leading=28, textColor=PRIMARY, spaceBefore=30, spaceAfter=12, fontName='Helvetica-Bold')
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=16, leading=22, textColor=ACCENT, spaceBefore=20, spaceAfter=8, fontName='Helvetica-Bold')
    body = ParagraphStyle('Body2', parent=styles['Normal'], fontSize=11, leading=17, textColor=DARK, spaceAfter=8, alignment=TA_JUSTIFY)
    prompt_style = ParagraphStyle('Prompt', parent=styles['Normal'], fontSize=11, leading=17, textColor=DARK, spaceAfter=6, leftIndent=20, backColor=LIGHT, borderPadding=8, borderRadius=3)
    caption = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=9, leading=13, textColor=GRAY, spaceAfter=6, alignment=TA_CENTER)
    return {
        'title': title, 'subtitle': subtitle, 'h1': h1, 'h2': h2,
        'body': body, 'prompt': prompt_style, 'caption': caption
    }

def make_prompt_doc(filename, title_text, subtitle_text, categories):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
        topMargin=0.8*inch, bottomMargin=0.8*inch,
        leftMargin=0.9*inch, rightMargin=0.9*inch)
    styles = build_styles()
    story = []
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph(title_text, styles['title']))
    story.append(Paragraph(subtitle_text, styles['subtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("How to Use This Guide", styles['h1']))
    story.append(Paragraph(
        "Each prompt is designed to be copied directly into ChatGPT, Claude, or any AI assistant. "
        "Replace the bracketed [like this] placeholders with your specific details. "
        "Every prompt includes a brief note on when and why to use it, so you can pick the right one for each task.",
        styles['body']
    ))
    story.append(PageBreak())

    prompt_num = 1
    for cat_name, cat_desc, prompts in categories:
        story.append(Paragraph(f"Category: {cat_name}", styles['h1']))
        story.append(Paragraph(cat_desc, styles['body']))
        story.append(Spacer(1, 0.2*inch))
        for p_title, p_text in prompts:
            story.append(Paragraph(f"<b>Prompt {prompt_num}: {p_title}</b>", styles['h2']))
            story.append(Paragraph(p_text, styles['prompt']))
            story.append(Spacer(1, 0.1*inch))
            prompt_num += 1
        story.append(PageBreak())

    doc.build(story)
    print(f"  Saved {filename} ({os.path.getsize(filename)} bytes)")


# ============================================================
# PDF 1: 100 AI Prompts for Content Creators
# ============================================================
def make_prompts_pdf():
    categories = [
        ("Blog Content", "Prompts for planning, drafting, and optimizing long-form content.", [
            ("Blog Post Outline Generator", "Act as a senior content strategist. Create a detailed blog post outline for the topic: [TOPIC]. Target audience: [AUDIENCE]. Include: 1) A compelling hook/opening, 2) 5-7 main sections with subpoints, 3) A conclusion with a clear CTA, 4) Suggested word counts per section, 3 internal linking opportunities, and 3 SEO keywords to naturally weave in."),
            ("SEO Blog Introduction", "Write a 150-word introduction for a blog post titled '[TITLE]'. Include the primary keyword [KEYWORD] within the first 100 words. Use a problem-agitation approach. Target audience: [AUDIENCE]. Tone: [TONE — e.g., professional, conversational, witty]."),
            ("Blog Conclusion with CTA", "Write a conclusion paragraph for a blog post about [TOPIC]. Summarize the 3 key takeaways, include a compelling call-to-action for [OFFER/SIGNUP], and end with an engagement question. Word count: 100-150 words."),
            ("Blog Title Generator", "Generate 10 click-worthy blog post titles for the topic [TOPIC]. Include: 3 how-to titles, 3 listicle titles, 2 question-based titles, and 2 curiosity-driven titles. Each title should be under 60 characters and include the keyword [KEYWORD] where natural."),
            ("Blog Meta Description", "Write 3 meta descriptions (150-160 characters each) for a blog post titled '[TITLE]' about [TOPIC]. Include the keyword [KEYWORD] in at least one. Make them compelling enough to earn clicks from search results."),
            ("Content Gap Analysis", "Act as an SEO content strategist. I'm creating content for [NICHE/INDUSTRY]. Analyze these competitor URLs: [URL1], [URL2], [URL3]. Identify 5 content gaps — topics they haven't covered that I should create content around. Rank by search volume potential."),
            ("Blog Post from Bullet Points", "Expand the following bullet points into a 1,500-word blog post. Maintain a [TONE] tone throughout. Add transitions, examples, and a strong conclusion.\n\nBullet points:\n• [POINT 1]\n• [POINT 2]\n• [POINT 3]\n• [POINT 4]\n• [POINT 5]"),
            ("FAQ Section Generator", "Generate an FAQ section with 8 questions and detailed answers (80-120 words each) for a blog post about [TOPIC]. Base these on real 'People Also Ask' style questions. Include schema-markup-ready formatting (question as H3, answer as paragraph)."),
            ("Blog Update & Refresh", "I have an existing blog post from [YEAR] about [TOPIC]. Here's the current content: [PASTE CONTENT]. Refresh this post for 2026: update statistics, add new insights, improve the intro, add a section on [NEW DEVELOPMENT], and suggest 3 new internal links."),
            ("Long-Form Research Brief", "Create a detailed content brief for a 3,000-word guide on [TOPIC]. Include: target keyword, 5 supporting keywords, search intent analysis, suggested H2/H3 structure, 3 expert quotes to source, 5 statistics to find, competitor content to review, and recommended word count per section."),
            ("Blog Post from Interview", "Turn this interview transcript into a polished 2,000-word blog post. Maintain the interviewee's voice while improving flow and readability. Add an introduction, subheadings, and a conclusion. Source: [PASTE TRANSCRIPT]."),
            ("Content Upgrade Generator", "Create a content upgrade (lead magnet) idea for a blog post about [TOPIC]. Include: title, format (checklist/template/cheat sheet), 3 key points to cover, and the opt-in CTA copy. Make it directly relevant to the post."),
            ("Blog Series Planner", "Plan a 5-part blog series on [TOPIC]. For each post: title, target keyword, main argument, and how it connects to the next post. Include an overarching narrative arc."),
            ("Internal Linking Strategy", "Analyze my existing blog posts: [LIST TITLES/URLS]. Suggest 10 internal linking opportunities between them. For each: source post, target post, and recommended anchor text. Prioritize by SEO impact."),
        ]),
        ("Social Media", "Prompts for crafting engaging posts, threads, and captions across platforms.", [
            ("Twitter/X Thread Generator", "Write a 10-tweet thread about [TOPIC]. Hook the reader in tweet 1 with a bold claim or surprising stat. Each tweet should be under 250 characters, end with a curiosity gap or transition, and the final tweet should include a CTA. Number each tweet."),
            ("LinkedIn Post Generator", "Write a LinkedIn post (1,300 characters max) about [TOPIC]. Use a personal story hook in the first 2 lines. Include line breaks between every 1-2 sentences for readability. End with a question to drive engagement. Target audience: [PROFESSIONAL AUDIENCE]."),
            ("Instagram Caption Generator", "Write 5 Instagram caption options for a post about [TOPIC/IMAGE DESCRIPTION]. Vary the lengths: 1 short (50 words), 2 medium (100-150 words), 2 long (200+ words). Include 5 relevant hashtags for each. Tone: [TONE]."),
            ("Social Media Content Calendar", "Create a 7-day content calendar for [BRAND/ACCOUNT] on [PLATFORM]. Include: post type, caption hook, visual suggestion, and best time to post. Mix educational, entertaining, and promotional content (40/40/20 ratio)."),
            ("Viral Hook Generator", "Generate 20 viral-style hooks for [PLATFORM] about [TOPIC]. Include: 5 'I tried X so you don't have to' hooks, 5 'X things I wish I knew' hooks, 5 'Stop doing X' hooks, and 5 'The truth about X' hooks."),
            ("Engagement Question Generator", "Generate 15 engagement-driving questions for [PLATFORM] related to [NICHE]. Mix: opinion polls, 'this or that' questions, personal experience prompts, and hot takes. Each question should invite comments, not just likes."),
            ("Instagram Reel Script", "Write a 60-second Instagram Reel script about [TOPIC]. Include: hook (first 3 seconds), 3 main points with timestamps, text overlays suggestion, and a CTA. Format: [HOOK] → [POINT 1] → [POINT 2] → [POINT 3] → [CTA]."),
            ("LinkedIn Carousel Script", "Write a 10-slide LinkedIn carousel about [TOPIC]. For each slide: title (max 40 words), body text (max 60 words), and visual suggestion. Slide 1 must be a curiosity-inducing hook. Slide 10 must be a clear CTA."),
            ("Twitter/X Bio Optimizer", "Rewrite this Twitter/X bio for maximum impact: [CURRENT BIO]. Niche: [NICHE]. Must include: what I do, who I help, social proof element, and a personality touch. Under 160 characters. Provide 5 options."),
            ("Social Proof Post Generator", "Create a social media post that shares a customer success story. Customer: [NAME], Problem: [PROBLEM], Solution: [YOUR PRODUCT/SERVICE], Result: [RESULT WITH NUMBERS]. Write it as a mini case study that sells without being salesy."),
            ("LinkedIn Newsletter Teaser", "Write a 3-sentence teaser for my LinkedIn Newsletter about [TOPIC]. The first sentence must create curiosity. The second must promise value. The third must include a 'Subscribe for more' CTA. Total: under 300 characters."),
            ("TikTok Script Generator", "Write a TikTok script (30-60 seconds) about [TOPIC]. Format: Hook → Context → Value (3 tips/facts) → CTA. Include visual directions and text overlays. Tone: energetic, fast-paced. Include suggested sounds/trends."),
            ("Pinterest Pin Description", "Write 5 Pinterest pin descriptions (250-300 characters each) for content about [TOPIC]. Include: 3-5 relevant keywords, a clear value proposition, and a CTA to click through. Format for Pinterest SEO."),
            ("YouTube Community Tab Post", "Write a YouTube Community Tab post (280 characters max) to engage my audience between video uploads. Topic: [TOPIC]. Include a question to drive comments. Suggest a poll option with 2 choices."),
            ("Cross-Platform Repurposing", "Take this [BLOG POST/TWEET/VIDEO TRANSCRIPT] and repurpose it for 3 platforms: Twitter (thread), LinkedIn (post), Instagram (carousel). Maintain the core message but adapt the format and tone for each platform. Source content: [PASTE]."),
            ("Social Media Bio for Creators", "Write 5 creator bio options for [PLATFORM]. Niche: [NICHE]. Include: authority statement, value proposition, personality trait, and CTA. Max character count: [PLATFORM LIMIT]. Include relevant emojis."),
            ("User-Generated Content Prompt", "Write a prompt I can send to my audience to encourage UGC about [PRODUCT/TOPIC]. Include: clear instructions, example response, incentive (if any), and hashtag. Make it easy and fun for followers to participate."),
            ("Social Listening Query", "Generate 10 search queries I can use to monitor conversations about [TOPIC/INDUSTRY] on social media. Include: competitor mentions, pain point discussions, and trending topic variations."),
            ("Social Media Report Summary", "Summarize these social media metrics into a 150-word performance overview for [PERIOD]. Highlight: top-performing content, growth trends, and 3 actionable insights. Metrics: [PASTE METRICS]."),
            ("Influencer Outreach Message", "Write a DM/email to collaborate with an influencer. Influencer: [NAME], Niche: [NICHE], Follower count: [COUNT]. Offer: [COLLAB DETAILS]. Keep it personal, specific, and low-pressure. Under 200 words."),
        ]),
        ("Video & Podcast Scripts", "Prompts for scripting YouTube videos, podcast episodes, and short-form content.", [
            ("YouTube Video Script", "Write a full YouTube video script (8-12 minutes) about [TOPIC]. Include: hook (first 15 seconds), intro with value promise, 5 main sections with timestamps, B-roll suggestions, and end screen CTA. Target audience: [AUDIENCE]."),
            ("Podcast Episode Outline", "Create a detailed outline for a 45-minute podcast episode about [TOPIC]. Include: cold open (2 min), intro (3 min), 4 main segments (8 min each), guest questions (if applicable), and outro with CTA. Add suggested sound effects/music cues."),
            ("YouTube Shorts Script", "Write 5 YouTube Shorts scripts (30-60 seconds each) about [TOPIC]. Each must: hook in first 2 seconds, deliver one clear value point, end with a follow CTA. Include text overlay suggestions and visual directions."),
            ("Podcast Intro Script", "Write a podcast intro script (60 seconds) for a show called [SHOW NAME] about [NICHE]. Include: host introduction, what listeners will learn today, episode teaser, and a subscribe CTA. Tone: [TONE]."),
            ("YouTube Description Generator", "Write a YouTube video description (2,000+ characters) for a video titled '[TITLE]' about [TOPIC]. Include: summary, 5+ timestamps, 3 related video links, social links, and 10+ relevant keywords naturally placed."),
            ("Podcast Show Notes", "Write detailed show notes for a podcast episode about [TOPIC]. Include: episode summary (100 words), 5 key takeaways, timestamped chapters, guest bio (if applicable), and 3 resources mentioned. Add links section."),
            ("Video Hook Generator", "Generate 10 video hooks for a YouTube video about [TOPIC]. Include: 3 pattern interrupts, 3 curiosity gaps, 2 bold claims, and 2 story openers. Each hook should be under 20 words and grab attention in the first 5 seconds."),
            ("Podcast Interview Questions", "Generate 15 interview questions for a podcast guest who is a [EXPERT TYPE] in [NICHE]. Mix: 5 icebreaker/personal questions, 5 expertise questions, 3 contrarian/hot-take questions, 2 audience-focused questions. Order them for natural conversation flow."),
            ("YouTube End Screen Script", "Write a 30-second end screen script for a YouTube video about [TOPIC]. Include: recap of key point, recommendation for next video (create curiosity), and subscribe CTA. Keep it conversational and energetic."),
            ("Podcast Ad Read Script", "Write a 60-second host-read ad script for [PRODUCT/SERVICE]. Include: personal connection to product, 3 key benefits, social proof, and a clear CTA with discount code [CODE]. Make it feel authentic, not salesy."),
            ("Video Chapter Timestamps", "Generate YouTube chapter timestamps for a video about [TOPIC]. Based on this outline: [OUTLINE]. Create 6-8 chapters with descriptive titles (max 40 chars each) and estimated timestamps."),
            ("Podcast Trailer Script", "Write a 90-second podcast trailer for [SHOW NAME]. Include: what the show is about, who it's for, host credibility, a teaser clip suggestion, and where to subscribe. End with a memorable tagline."),
            ("YouTube Community Post", "Write a YouTube Community Tab post to promote my latest video about [TOPIC]. Include: teaser of the value, link to video, and a question to drive comments. Under 280 characters."),
            ("Podcast Cold Open", "Write a 2-minute cold open for a podcast episode about [TOPIC]. Start with a compelling story or surprising fact that hooks the listener. Transition smoothly into the intro music and episode content."),
            ("Video B-Roll Suggestions", "For a YouTube video about [TOPIC] with these main points: [POINTS], suggest 10 B-roll shots, text overlays, or graphics that would enhance viewer engagement. Include timestamps for each suggestion."),
        ]),
            ("Email & Newsletter", "Prompts for writing emails that get opened, read, and clicked.", [
            ("Welcome Email Sequence", "Write a 5-email welcome sequence for new subscribers to [BRAND/NEWSLETTER]. Email 1: Welcome + deliver lead magnet. Email 2: My story + mission. Email 3: Best content roundup. Email 4: Social proof + case study. Email 5: Soft pitch for [OFFER]. Each email: 150-250 words."),
            ("Subject Line Generator", "Generate 20 email subject lines for a newsletter about [TOPIC]. Include: 5 curiosity-driven, 5 urgency/scarcity, 5 benefit-driven, 5 personal/story-based. Each under 50 characters. Indicate open rate potential (high/medium)."),
            ("Abandoned Cart Email", "Write a 3-email abandoned cart sequence for [PRODUCT]. Email 1 (1 hour later): Reminder + product image. Email 2 (24 hours): Address objections + social proof. Email 3 (72 hours): Urgency + discount offer. Each under 150 words."),
            ("Newsletter Edition", "Write a newsletter edition (500-700 words) for [BRAND] about [TOPIC]. Include: personal opening story, 3 main insights with actionable takeaways, a recommended resource, and a P.S. with a CTA. Tone: [TONE]."),
            ("Product Launch Email", "Write a launch email for [PRODUCT NAME]. Include: problem agitation, solution reveal, 3 key benefits, social proof element, pricing, and urgency CTA. Length: 200-300 words. Make it feel like an event, not a sales pitch."),
            ("Re-engagement Email", "Write a 2-email re-engagement sequence for inactive subscribers (no opens in 90 days). Email 1: 'We miss you' + best content roundup. Email 2: 'Last chance' + exclusive offer or unsubscribe option. Tone: warm, not guilt-trippy."),
            ("Email Signature Generator", "Create 5 email signature options for [NAME], [TITLE] at [COMPANY]. Include: name, title, company, one social link, and a subtle CTA. Keep it clean and professional. Max 4 lines each."),
            ("Cold Outreach Email", "Write a cold outreach email to [PROSPECT TYPE] about [OFFER/VALUE PROP]. Include: personalized opener, clear value proposition, social proof, and a low-friction CTA. Under 150 words. Make it about them, not you."),
            ("Email A/B Test Ideas", "Generate 10 A/B test ideas for my email about [TOPIC]. For each: variable to test, hypothesis, and what to measure. Include subject line tests, CTA tests, and content format tests."),
            ("Thank You Email", "Write a post-purchase thank you email for [PRODUCT]. Include: genuine gratitude, what to expect next, usage tips, and a referral ask. Under 150 words. Make the customer feel great about their decision."),
            ("Email Preheader Text", "Write 5 preheader text options (80-100 characters each) for an email with subject line '[SUBJECT]'. Each should complement (not repeat) the subject line and increase open rates."),
            ("Survey Email", "Write an email asking subscribers to fill out a [TYPE] survey. Include: why their input matters, how long it takes (under 3 min), incentive (if any), and a clear CTA button text. Under 120 words."),
            ("Affiliate Promotion Email", "Write an email promoting [AFFILIATE PRODUCT] to my audience interested in [NICHE]. Include: personal experience, 3 specific benefits, honest assessment, and affiliate disclosure. Under 200 words."),
            ("Milestone Celebration Email", "Write an email celebrating a milestone: [MILESTONE DETAILS]. Include: reflection on the journey, thank you to subscribers, exclusive bonus/gift, and what's next. Make subscribers feel part of the win."),
            ("Email Automation Trigger", "Design an email automation trigger for [BEHAVIOR/ACTION]. Include: trigger condition, delay timing, email content outline, and exit condition. Describe the full flow in 150 words."),
        ]),
        ("Strategy & Planning", "Prompts for content strategy, audience research, and growth planning.", [
            ("Content Strategy Blueprint", "Create a 90-day content strategy for [BRAND/CREATOR] in [NICHE]. Include: content pillars (3-4), weekly posting schedule, platform mix, content types per platform, and KPIs to track. Target audience: [AUDIENCE]."),
            ("Audience Persona Generator", "Create 3 detailed audience personas for [NICHE/INDUSTRY]. For each: demographics, psychographics, pain points, goals, content preferences, platforms they use, and a day-in-the-life snapshot. Make them actionable for content creation."),
            ("Competitor Content Analysis", "Analyze the content strategy of [COMPETITOR NAME/URL]. Identify: their top 5 performing content pieces, content gaps they're missing, their posting frequency, engagement patterns, and 3 opportunities for me to differentiate."),
            ("Content Pillar Generator", "Generate 5 content pillars for a [NICHE] brand. For each pillar: 3 subtopics, 5 post ideas, target keyword, and content format recommendations. Ensure pillars cover educational, entertaining, and promotional angles."),
            ("30-Day Content Calendar", "Create a 30-day content calendar for [BRAND] on [PLATFORMS]. Include: daily post topic, content format, platform, caption hook, and CTA. Balance: 40% educational, 30% entertaining, 20% promotional, 10% community."),
            ("Brand Voice Generator", "Define a brand voice guide for [BRAND NAME] in [NICHE]. Include: 3 voice characteristics with examples, do's and don'ts, sample sentences showing the voice, and how it adapts across platforms (Twitter vs. LinkedIn vs. email)."),
            ("Content Repurposing Plan", "Create a repurposing plan for this piece of content: [DESCRIBE/PASTE]. Show how to turn it into: 1 blog post, 5 social posts, 1 email, 1 video script, and 1 infographic outline. Maximize value from one core idea."),
            ("Viral Content Analysis", "Analyze why this content went viral: [DESCRIBE/LINK]. Identify: the emotional trigger, the shareability factor, the timing element, and 3 lessons I can apply to my own content in [NICHE]."),
            ("Content Audit Framework", "Create a content audit framework for my [BLOG/CHANNEL]. Include: metrics to evaluate (traffic, engagement, conversions), a scoring system (1-5), criteria for updating vs. deleting, and a prioritization matrix for content updates."),
            ("Growth Strategy Roadmap", "Create a 6-month growth strategy for [BRAND/CREATOR] on [PLATFORM]. Include: monthly goals, content experiments to run, collaboration opportunities, paid strategy (if applicable), and milestone metrics. Current stats: [STATS]."),
            ("Content ROI Calculator", "Help me calculate the ROI of my content marketing. Provide a framework that accounts for: time investment, tool costs, traffic generated, leads converted, and revenue attributed. Include a simple formula I can reuse."),
            ("Editorial Guidelines", "Write editorial guidelines for my content team at [BRAND]. Include: brand voice rules, formatting standards, image guidelines, fact-checking process, approval workflow, and common mistakes to avoid. Make it a practical reference document."),
            ("Content Experiment Design", "Design a content experiment to test [HYPOTHESIS]. Include: control and variant, success metrics, sample size needed, duration, and how to analyze results. Make it statistically sound but practical for a small team."),
            ("Influencer Strategy Plan", "Create an influencer marketing strategy for [BRAND] in [NICHE]. Include: influencer tiers to target, outreach approach, collaboration types, budget allocation, and KPIs. Focus on micro-influencers (10K-100K followers)."),
            ("Content Monetization Plan", "Generate 5 monetization strategies for my content in [NICHE]. For each: revenue model, implementation steps, estimated revenue potential, and time to first dollar. Consider: digital products, services, ads, affiliates, and sponsorships."),
            ("Annual Content Audit Plan", "Create an annual content audit plan for my [BLOG/CHANNEL]. Include: quarterly review schedule, metrics to track, content scoring rubric, pruning criteria, and a workflow for updating or consolidating old content."),
        ]),
        ("SEO & Optimization", "Prompts for search engine optimization and content discoverability.", [
            ("Keyword Research Brief", "Create a keyword research brief for [NICHE]. Include: 10 primary keywords with search volume estimates, 15 long-tail variations, keyword difficulty assessment, and content recommendations for each. Target audience: [AUDIENCE]."),
            ("Meta Tags Generator", "Write optimized meta title (50-60 chars) and meta description (150-160 chars) for a page about [TOPIC]. Include primary keyword [KEYWORD] and secondary keyword [KEYWORD2]. Make them compelling for click-through."),
            ("Schema Markup Generator", "Generate JSON-LD schema markup for a [TYPE: FAQ/HowTo/Article/Product] page about [TOPIC]. Include all required properties for Google rich results. Format as valid JSON."),
            ("Image Alt Text Generator", "Write SEO-optimized alt text for 10 images related to [TOPIC]. Each alt text should: be under 125 chars, describe the image accurately, include a keyword where natural, and be accessible. Image descriptions: [LIST]."),
            ("URL Slug Generator", "Generate 10 SEO-friendly URL slugs for content about [TOPIC]. Each should: be under 60 chars, include the target keyword, use hyphens not underscores, be readable, and avoid stop words."),
            ("Internal Link Audit", "Analyze these page titles and suggest internal linking opportunities: [LIST]. For each link: source page, target page, anchor text, and SEO value (high/medium/low). Focus on distributing link equity to important pages."),
            ("Content Brief from Keyword", "Create a detailed content brief based on the keyword [KEYWORD]. Include: search intent analysis, 5 questions to answer, 3 competitor URLs to analyze, suggested word count, and 5 LSI keywords to include."),
            ("Featured Snippet Optimizer", "Optimize this content to win a featured snippet for [KEYWORD]. Include: a 40-60 word paragraph answer, a numbered list version, and a table format version. Source content: [PASTE]."),
            ("SERP Analysis Prompt", "Analyze the current Google SERP for [KEYWORD]. Identify: the dominant content format, common headings across top 10 results, missing angles, and opportunities to differentiate my content."),
            ("E-E-A-T Signals Audit", "Review this content for E-E-A-T (Experience, Expertise, Authority, Trust) signals: [PASTE CONTENT]. Identify gaps and suggest improvements for each pillar. Add specific places to inject personal experience and credentials."),
            ("Page Speed Content Audit", "Review my content-heavy page and identify elements that may slow loading: [URL/CONTENT]. Suggest: image optimization, lazy loading opportunities, deferred scripts, and content prioritization for faster LCP."),
            ("Local SEO Content Generator", "Write 5 pages of location-based content for [BUSINESS TYPE] in [LOCATION]. Each page: 500-700 words, includes local keywords, NAP consistency, and location-specific value. Target: local pack visibility."),
            ("Compelling Product Descriptions", "Write 5 product e-commerce descriptions for [PRODUCT TYPE]. Each: 100-150 words, includes features + benefits, addresses objections, includes social proof hook, and ends with CTA. Optimized for both users and search."),
            ("Category Page Copy", "Write SEO-optimized copy for a category page about [CATEGORY]. Include: H1 tag, introductory paragraph (150 words), product grid description, sidebar content, and internal links. Target keyword: [KEYWORD]."),
            ("Broken Link Building Brief", "Create a broken link building campaign for [NICHE]. Include: 10 resource page targets, suggested replacement content topics, outreach email template, and tracking spreadsheet structure."),
            ("YouTube SEO Optimization", "Optimize my YouTube video for search. Title: [TITLE], Topic: [TOPIC]. Provide: optimized title, 2000+ character description, 15 tags, and 5 timestamped chapters. Target keyword: [KEYWORD]."),
            ("Podcast SEO Show Notes", "Create SEO-optimized podcast show notes for an episode about [TOPIC]. Include: keyword-rich title, 300-word summary, timestamped chapters with keywords, guest links, and 5 related episode links."),
            ("Competitor Backlink Analysis", "Analyze the backlink profile of [COMPETITOR URL]. Identify: top 10 referring domains, 5 linkable assets they've created, broken link opportunities, and guest post targets. Provide a prioritized action plan."),
            ("Google Business Profile Posts", "Write 5 Google Business Profile posts for [BUSINESS TYPE]. Each: 150-300 words, includes relevant keywords, has a CTA, and aligns with [PROMOTION/EVENT/UPDATE]. Include image suggestions for each."),
            ("Review Generation Message", "Write a review request message for [PRODUCT/SERVICE]. Include: timing recommendation, personalization tokens, direct review link, and a 2-step follow-up sequence. Make it feel natural, not transactional."),
        ]),
    ]

    # Flatten to verify we have 100 prompts
    total = sum(len(prompts) for _, _, prompts in categories)
    assert total >= 95, f"Expected ~100 prompts, got {total}"
    print(f"Total prompts: {total}")

    make_prompt_doc(
        '/home/brettanthonysjoberg179/100-AI-Prompts-for-Content-Creators.pdf',
        '100 AI Prompts for Content Creators',
        'The Ultimate Prompt Library for Bloggers, YouTubers, Podcasters & Social Media Managers',
        categories
    )


# ============================================================
# PDF 2: Digital Product Launch Kit
# ============================================================
def make_launch_kit_pdf():
    doc = SimpleDocTemplate(
        '/home/brettanthonysjoberg179/Digital-Product-Launch-Kit.pdf',
        pagesize=LETTER,
        topMargin=0.8*inch, bottomMargin=0.8*inch,
        leftMargin=0.9*inch, rightMargin=0.9*inch
    )
    styles = build_styles()
    story = []

    # Cover
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Digital Product Launch Kit", styles['title']))
    story.append(Paragraph("The Complete System to Launch Your First (or Next) Digital Product in 30 Days", styles['subtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Validation → MVP → Pricing → Launch → Scale", styles['h2']))
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("Table of Contents", styles['h1']))
    toc_items = [
        "Section 1: Validation Framework",
        "Section 2: MVP Workflow",
        "Section 3: Pricing Strategy",
        "Section 4: Launch Sequence",
        "Section 5: Email Automation Templates",
        "Section 6: Landing Page Templates",
        "Section 7: Launch Checklists",
        "Section 8: Post-Launch Optimization",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['body']))
    story.append(PageBreak())

    # Section 1
    story.append(Paragraph("Section 1: Validation Framework", styles['h1']))
    story.append(Paragraph("Before you build anything, validate that people will pay for your idea. This framework saves you from building products nobody wants.", styles['body']))
    story.append(Paragraph("The 3-Step Validation Process", styles['h2']))
    story.append(Paragraph("<b>Step 1: Problem Interviews (Days 1-3)</b>", styles['h2']))
    story.append(Paragraph("Talk to 10-15 people in your target market. Don't pitch your solution — just understand their problem. Ask:", styles['body']))
    story.append(Paragraph("• What's the hardest part about [PROBLEM AREA]?<br/>• How are you currently solving this?<br/>• What frustrates you about current solutions?<br/>• How much time/money does this problem cost you?<br/>• Have you tried to solve this before? What happened?", styles['prompt']))
    story.append(Paragraph("<b>Step 2: Smoke Test (Days 4-7)</b>", styles['h2']))
    story.append(Paragraph("Create a simple landing page describing your product and drive traffic. Measure:", styles['body']))
    story.append(Paragraph("• Email signup rate (target: 10%+ of visitors)<br/>• Click-through on 'Buy' button (even if product doesn't exist yet)<br/>• Comments and questions from visitors<br/>• Social media engagement on launch-related posts", styles['prompt']))
    story.append(Paragraph("<b>Step 3: Pre-Sale (Days 8-10)</b>", styles['h2']))
    story.append(Paragraph("Offer a 'founding member' discount to your email list. Even 5-10 sales prove demand. If you can't get 5 sales, pivot the idea before building.", styles['body']))
    story.append(PageBreak())

    # Section 2
    story.append(Paragraph("Section 2: MVP Workflow", styles['h1']))
    story.append(Paragraph("Build the smallest version of your product that delivers real value. Ship fast, improve later.", styles['body']))
    story.append(Paragraph("MVP Scope Definition", styles['h2']))
    story.append(Paragraph("List every feature you imagine. Now cut 80%. The remaining 20% is your MVP. Ask: 'If I could only deliver ONE transformation, what would it be?'", styles['body']))
    story.append(Paragraph("MVP Build Timeline (14 Days)", styles['h2']))
    story.append(Paragraph("• <b>Days 1-3:</b> Outline the core content/modules<br/>• <b>Days 4-7:</b> Create the first draft of each module<br/>• <b>Days 8-10:</b> Format and polish (PDF, templates, worksheets)<br/>• <b>Days 11-12:</b> Create bonus materials (cheat sheets, checklists)<br/>• <b>Days 13-14:</b> Final review and upload to Gumroad", styles['prompt']))
    story.append(Paragraph("MVP Quality Standards", styles['h2']))
    story.append(Paragraph("Your MVP doesn't need to be perfect, but it must be complete and actionable. Before launching, verify:", styles['body']))
    story.append(Paragraph("• Every promise in your sales copy is fulfilled<br/>• All links, downloads, and resources work<br/>• The product is easy to consume (clear structure, good formatting)<br/>• A beginner can follow it without additional help<br/>• It delivers at least one clear, measurable result", styles['prompt']))
    story.append(PageBreak())

    # Section 3
    story.append(Paragraph("Section 3: Pricing Strategy", styles['h1']))
    story.append(Paragraph("Price based on value delivered, not time invested. Here's how to find your price.", styles['body']))
    story.append(Paragraph("The Value-Based Pricing Formula", styles['h2']))
    story.append(Paragraph("1. What's the outcome worth to your customer? (e.g., $500 value)<br/>2. What's the next cheapest alternative? (e.g., $200 course)<br/>3. Price at 10-25% of the value created = $50-$125", styles['prompt']))
    story.append(Paragraph("Pricing Tiers", styles['h2']))
    story.append(Paragraph("• <b>Basic ($17-$37):</b> Core product only (PDF, templates, guide)<br/>• <b>Standard ($47-$97):</b> Core + bonus materials + templates<br/>• <b>Premium ($147-$297):</b> Everything + community access or 1:1 call", styles['prompt']))
    story.append(Paragraph("Psychological Pricing Tactics", styles['h2']))
    story.append(Paragraph("• Use charm pricing ($47, $97) not round numbers<br/>• Show the 'value stack' total ($500+ value for $47)<br/>• Offer a 'founding member' discount for early buyers<br/>• Create urgency with limited-time bonuses, not fake scarcity<br/>• Include a money-back guarantee to reduce risk", styles['prompt']))
    story.append(PageBreak())

    # Section 4
    story.append(Paragraph("Section 4: Launch Sequence", styles['h1']))
    story.append(Paragraph("A structured 14-day launch sequence that builds momentum and maximizes sales.", styles['body']))
    story.append(Paragraph("Pre-Launch (Days 1-7)", styles['h2']))
    story.append(Paragraph("• Day 1-2: Tease the problem on social media<br/>• Day 3-4: Share your story and why you're building this<br/>• Day 5: Reveal the product (sneak peek)<br/>• Day 6: Share testimonials or beta results<br/>• Day 7: Open cart with founding member discount", styles['prompt']))
    story.append(Paragraph("Launch Week (Days 8-14)", styles['h2']))
    story.append(Paragraph("• Day 8: Launch email + social posts (main push)<br/>• Day 9: Address FAQs and objections<br/>• Day 10: Share a case study or walkthrough<br/>• Day 11: Mid-launch bonus announcement<br/>• Day 12: Social proof showcase (testimonials, screenshots)<br/>• Day 13: Last chance reminder (cart closing)<br/>• Day 14: Cart close + thank you to buyers", styles['prompt']))
    story.append(PageBreak())

    # Section 5
    story.append(Paragraph("Section 5: Email Automation Templates", styles['h1']))
    story.append(Paragraph("Copy-paste email templates for your entire launch sequence.", styles['body']))
    story.append(Paragraph("Email 1: The Problem Tease", styles['h2']))
    story.append(Paragraph("Subject: The #1 mistake [AUDIENCE] makes with [PROBLEM]<br/><br/>Hey [NAME],<br/><br/>I noticed something weird about [INDUSTRY/PROBLEM AREA].<br/><br/>Most [AUDIENCE] think [COMMON MISCONCEPTION]. But that's exactly why [NEGATIVE OUTCOME].<br/><br/>I've been testing a different approach, and the results have been surprising.<br/><br/>More tomorrow.<br/><br/>[YOUR NAME]", styles['prompt']))
    story.append(Paragraph("Email 2: The Story", styles['h2']))
    story.append(Paragraph("Subject: Why I almost gave up on [GOAL]<br/><br/>Hey [NAME],<br/><br/>Six months ago, I was stuck. [SHORT PERSONAL STORY OF STRUGGLE].<br/><br/>I tried [FAILED APPROACH 1]. Didn't work.<br/>I tried [FAILED APPROACH 2]. Also didn't work.<br/><br/>Then I discovered [INSIGHT/BREAKTHROUGH].<br/><br/>Tomorrow I'm sharing exactly what I built — and why it's going to change everything for [AUDIENCE].<br/><br/>Stay tuned.<br/><br/>[YOUR NAME]", styles['prompt']))
    story.append(Paragraph("Email 3: The Reveal", styles['h2']))
    story.append(Paragraph("Subject: Introducing [PRODUCT NAME] 🚀<br/><br/>Hey [NAME],<br/><br/>It's finally here.<br/><br/>[PRODUCT NAME] is [ONE-LINE DESCRIPTION].<br/><br/>Here's what's inside:<br/>✅ [BENEFIT 1]<br/>✅ [BENEFIT 2]<br/>✅ [BENEFIT 3]<br/>✅ [BONUS]<br/><br/>As a founding member, you get [DISCOUNT/PERCENT] off the regular price.<br/><br/>[LINK TO PRODUCT]<br/><br/>[YOUR NAME]", styles['prompt']))
    story.append(Paragraph("Email 4: The Objection Handler", styles['h2']))
    story.append(Paragraph("Subject: 'Is this worth it?' — let me answer that<br/><br/>Hey [NAME],<br/><br/>I've been getting questions about [PRODUCT NAME], so let me address the top 3:<br/><br/>❓ 'I'm not sure this is for me.'<br/>→ [PRODUCT] is designed for [SPECIFIC AUDIENCE]. If you're [CRITERIA], this is for you.<br/><br/>❓ 'Is it worth the investment?'<br/>→ The value inside is worth $[VALUE]. You're getting it for $[PRICE]. That's [X]% off.<br/><br/>❓ 'What if it doesn't work for me?'<br/>→ [GUARANTEE PERIOD]-day money-back guarantee. No questions asked.<br/><br/>[LINK TO PRODUCT]<br/><br/>[YOUR NAME]", styles['prompt']))
    story.append(Paragraph("Email 5: The Last Chance", styles['h2']))
    story.append(Paragraph("Subject: ⏰ Cart closes tonight<br/><br/>Hey [NAME],<br/><br/>Just a heads up — the founding member pricing for [PRODUCT NAME] ends tonight at midnight.<br/><br/>After that, the price goes up to [REGULAR PRICE].<br/><br/>If you've been on the fence, now's the time.<br/><br/>[LINK TO PRODUCT]<br/><br/>To your success,<br/>[YOUR NAME]", styles['prompt']))
    story.append(PageBreak())

    # Section 6
    story.append(Paragraph("Section 6: Landing Page Templates", styles['h1']))
    story.append(Paragraph("The anatomy of a high-converting product landing page.", styles['body']))
    story.append(Paragraph("Landing Page Structure", styles['h2']))
    story.append(Paragraph("1. <b>Hero Section:</b> Headline (clear benefit) + Subheadline (who it's for) + CTA button<br/>2. <b>Problem Section:</b> Agitate the pain point your audience faces<br/>3. <b>Solution Section:</b> Introduce your product as the answer<br/>4. <b>What's Inside:</b> Bullet list of everything included<br/>5. <b>Social Proof:</b> Testimonials, numbers, logos<br/>6. <b>About Section:</b> Your story and why you built this<br/>7. <b>FAQ Section:</b> Address objections<br/>8. <b>Final CTA:</b> Last chance to buy with urgency", styles['prompt']))
    story.append(Paragraph("Headline Formulas", styles['h2']))
    story.append(Paragraph("• 'Get [DESIRED OUTCOME] without [PAIN POINT]'<br/>• 'The [ADJECTIVE] Guide to [DESIRED OUTCOME] for [AUDIENCE]'<br/>• 'How [AUDIENCE] Can [DESIRED OUTCOME] in [TIMEFRAME]'<br/>• '[NUMBER] [RESOURCES] to Help You [DESIRED OUTCOME]'", styles['prompt']))
    story.append(Paragraph("CTA Button Copy", styles['h2']))
    story.append(Paragraph("• 'Get Instant Access'<br/>• 'Download Now — $[PRICE]'<br/>• 'Yes! I Want [OUTCOME]'<br/>• 'Join [NUMBER]+ [AUDIENCE] Who Already Use This'", styles['prompt']))
    story.append(PageBreak())

    # Section 7
    story.append(Paragraph("Section 7: Launch Checklists", styles['h1']))
    story.append(Paragraph("Print these checklists and tick them off as you go.", styles['body']))
    story.append(Paragraph("Pre-Launch Checklist (7 Days Before)", styles['h2']))
    story.append(Paragraph("☐ Product finalized and uploaded to Gumroad<br/>☐ Landing page live and tested<br/>☐ Email sequence written and scheduled<br/>☐ Social media posts drafted<br/>☐ Pricing and payment confirmed<br/>☐ Test purchase completed (verify download works)<br/>☐ Thank you page configured<br/>☐ Analytics tracking set up", styles['prompt']))
    story.append(Paragraph("Launch Day Checklist", styles['h2']))
    story.append(Paragraph("☐ Send launch email (morning)<br/>☐ Post on all social platforms<br/>☐ Respond to every comment within 1 hour<br/>☐ Monitor Gumroad dashboard for sales<br/>☐ Send personal thank you to first 10 buyers<br/>☐ Share buyer milestones on social ('5 copies sold!')<br/>☐ Check all links and downloads are working<br/>☐ Engage in relevant communities (don't spam)", styles['prompt']))
    story.append(Paragraph("Post-Launch Checklist (7 Days After)", styles['h2']))
    story.append(Paragraph("☐ Send thank you email to all buyers<br/>☐ Request testimonials/reviews<br/>☐ Analyze what worked and what didn't<br/>☐ Plan next launch or evergreen funnel<br/>☐ Update product based on buyer feedback<br/>☐ Set up email automation for future buyers<br/>☐ Celebrate your launch! 🎉", styles['prompt']))
    story.append(PageBreak())

    # Section 8
    story.append(Paragraph("Section 8: Post-Launch Optimization", styles['h1']))
    story.append(Paragraph("Your launch is just the beginning. Here's to optimize and scale.", styles['body']))
    story.append(Paragraph("Key Metrics to Track", styles['h2']))
    story.append(Paragraph("• <b>Conversion Rate:</b> Visitors to buyers (target: 1-3%)<br/>• <b>Email Open Rate:</b> Launch emails (target: 30-50%)<br/>• <b>Email Click Rate:</b> To landing page (target: 5-10%)<br/>• <b>Revenue Per Email:</b> Total sales ÷ list size<br/>• <b>Refund Rate:</b> Keep under 5%", styles['prompt']))
    story.append(Paragraph("Optimization Experiments", styles['h2']))
    story.append(Paragraph("• A/B test your landing page headline<br/>• Test different price points (charm pricing vs. round)<br/>• Try different email subject lines<br/>• Experiment with bonus offers vs. discount offers<br/>• Test long-form vs. short-form sales pages", styles['prompt']))
    story.append(Paragraph("Evergreen Funnel Setup", styles['h2']))
    story.append(Paragraph("After your launch, convert your product to evergreen:", styles['body']))
    story.append(Paragraph("1. Replace 'founding member' messaging with evergreen value proposition<br/>2. Set up an automated email sequence for new subscribers<br/>3. Create a tripwire offer ($7-$17) to capture buyers<br/>4. Add an upsell sequence after purchase<br/>5. Run periodic 'flash sales' to re-engage your list", styles['prompt']))

    doc.build(story)
    print(f"  Saved Digital-Product-Launch-Kit.pdf ({os.path.getsize('/home/brettanthonysjoberg179/Digital-Product-Launch-Kit.pdf')} bytes)")


if __name__ == '__main__':
    print("Generating PDFs...")
    make_prompts_pdf()
    make_launch_kit_pdf()
    print("Done!")
