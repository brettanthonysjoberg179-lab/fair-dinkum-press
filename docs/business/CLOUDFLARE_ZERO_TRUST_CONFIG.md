# 🔒 Cloudflare Access Zero Trust Configuration Guide

Date: October 7, 2026  
Project: Fair Dinkum Publishing & AI Advisory — Agent Control Center Security

---

## Overview
To protect your internal agent control centers, financial ledgers (`outputs/control_centre/`), and webhook administration endpoints from unauthorized access, we implement **Cloudflare Access (Zero Trust)**.

---

## 🛠️ Step-by-Step Implementation

### 1. Enable Cloudflare Zero Trust (Teams)
1. Log in to the [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/).
2. Select your team name or create your Zero Trust team domain (e.g., `fair-dinkum.cloudflareaccess.com`).

### 2. Configure Identity Providers (IdP)
1. Navigate to **Settings** > **Authentication**.
2. Add login methods:
   - **One-Time PIN (OTP)** via Email (fastest & most secure for solo operators).
   - **GitHub / Google Workspace** (for team-shared access).

### 3. Create an Access Application for the Control Center
1. Navigate to **Access** > **Applications** > **Add an application**.
2. Select **Self-Hosted**.
3. Configure Application Settings:
   - **Application Name:** `Fair Dinkum Agent Control Center`
   - **Subdomain:** `control.fairdinkum.publishing` (or your chosen hostname)
   - **Session Duration:** `24 hours`

### 4. Define Access Policies
Create a strict access rule ensuring only authorized administrators can reach the terminal and ledger endpoints:
* **Policy Name:** `Authorized Founders & Agents Only`
* **Action:** `Allow`
* **Include Rules:**
  - **Emails:** `brett@fairdinkum.publishing` (or your verified operational email address)
  - **Login Method:** One-Time PIN / GitHub OAuth

### 5. Bypass Rules for Webhooks & Public Storefronts
Ensure public webhooks and asset downloads remain publicly accessible to payment gateways (Stripe & Gumroad):
* Add a **Bypass** rule for paths:
  - `https://control.fairdinkum.publishing/webhook/*`
  - `https://control.fairdinkum.publishing/download/*`
  - `https://control.fairdinkum.publishing/health`
