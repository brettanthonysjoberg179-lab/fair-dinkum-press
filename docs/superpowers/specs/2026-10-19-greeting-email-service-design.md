# Warm & Professional Greeting Email Service Design Specification

## 1. Overview & Objectives
This service automates the delivery of personalized, warm, and professional greeting emails for **Birthdays**, **Christmas**, **Easter**, **Valentine's Day**, and **Halloween**. It allows users to manage contacts, assign personal relationships/notes, and automatically dispatches tailored holiday greetings on the exact dates via Gmail / SMTP.

---

## 2. Supported Occasion Templates
- **Birthday**: Celebrates professional milestones, personal growth, and wishes a successful year ahead.
- **Christmas**: Expresses gratitude for the year's collaboration/friendship and wishes a restful holiday season.
- **Easter**: Wishes renewal, fresh perspectives, and a joyful spring/autumn break.
- **Valentine's Day**: Warm appreciation for partnership, support, and professional/personal camaraderie.
- **Halloween**: Fun yet professional note wishing a wonderful spooky season and treats.

---

## 3. Architecture & Tech Stack
- **Language & Runtime**: Python 3.11+, SQLite for contact and dispatch state management.
- **Scheduler**: APScheduler / Daily cron job checking contact birthdays and holiday calendar triggers.
- **Email Dispatch**: Gmail API / SMTP integration.
- **Template Engine**: Jinja2 or Python f-strings with warm, professional tone variables (`{sender_name}`, `{recipient_name}`, `{relationship_note}`).

---

## 4. Database Schema
- `contacts`: `id`, `name`, `email`, `birthday` (MM-DD), `relationship`
- `dispatch_logs`: `id`, `contact_id`, `occasion`, `sent_date`, `status`
