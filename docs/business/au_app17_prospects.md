# AU APP 1.7 ADM Disclosure Gap — 6 Verified Prospects
(Checked live; all HTTP 200. Every email below was literally observed in the fetched page HTML.)

## 1. Medibank Private Limited
- Homepage: https://www.medibank.com.au
- Privacy policy: https://www.medibank.com.au/privacy/
- ADM gap: ZERO occurrences of "automated", "algorithm", "artificial intelligence", "profiling" anywhere in the policy (47,487 chars, 19 numbered sections). The policy describes collection/use/reasonableness/OAIC complaints in detail but never names ADM. Nearest thing is generic: "we also collect information about the technology you're using to access our apps."
- Email (seen on own site): privacy@medibank.com.au

## 2. Bupa Australia
- Homepage: https://www.bupa.com.au
- Privacy policy: https://www.bupa.com.au/help/privacy-and-security-trust-centre/privacy
- ADM gap: No "automated"/"algorithm"/"AI"/"profiling" in the policy text; only generic "How do we use your information" framing. Note: the full policy is partly hydrated by JS, so treat this as "not found in published policy" rather than proof of absence — but nothing ADM-related is exposed to the public at all.
- Email: NOT_FOUND (no email on the privacy page, help page or about page; only scams@bupa.com.au / stopfraud@bupa.com.au from the scams section). Use the Privacy & Security Trust Centre web form.

## 3. HCF
- Homepage: https://www.hcf.com.au
- Privacy policy: https://www.hcf.com.au/about-us/about-HCF/governance-and-structure/policies/privacy-policy
- ADM gap: ZERO occurrences of "automated", "algorithm", "artificial intelligence". Only "profil" once (in "change your profile settings") and "scor" twice — both in "health score from HCF Healthful" and "sleep score", i.e. member health metrics, not decisioning. Policy says only "conduct market research, customer surveys and data analytics" and "design, implement, promote and evaluate these programs". No purpose/how-it-works/effect disclosure.
- Email (seen on own site): privacyofficer@hcf.com.au

## 4. AIA Australia
- Homepage: https://www.aia.com.au
- Privacy policy: https://www.aia.com.au/en/privacy-policy
- ADM gap: Zero "automated"/"algorithm"/"AI". "profil" x4 but only as "form a single view of your customer/member profile" — i.e. data consolidation, explicitly not ADM. Underwriting and claims assessment are listed as purposes with no mention of automation, logic, inputs or effect.
- Email: NOT_FOUND (none published anywhere on aia.com.au; use the /en/privacy-policy complaint process)

## 5. Australian Unity
- Homepage: https://www.australianunity.com.au
- Privacy policy: https://www.australianunity.com.au/privacy-policy
- ADM gap: Best near-miss. They define AI in a glossary — "artificial intelligence (ai) is the ability of a system to perform tasks that normally require human intelligence" — but that is a glossary definition only. The purpose section says only "improve the service you receive and assess your eligibility for Australian Unity Limited (AUL) membership". No ADM section, no logic/inputs/effect explanation. Glossary presence without a substantive disclosure is still non-compliant.
- Email (seen on own site): GGSLegal@australianunity.com.au (from their legal-notices page; privacy officer enquiries@oaic.gov.au is the regulator, not theirs)

## 6. Amplar Health (formerly My Health Management / health fund services)
- Homepage: https://amplarhealth.com.au
- Privacy policy: https://amplarhealth.com.au/privacy/
- ADM gap: Complete absence — zero occurrences of "automated", "algorithm", "AI", "profiling" in the 21,308-char policy. Pure APP 3-13 boilerplate with no ADM content at all.
- Email (seen on own site): privacy@amplarhealth.com.au

---

## Considered but EXCLUDED (already compliant / partial)
- **Guild Insurance** — https://www.guildinsurance.com.au/privacy — has a real section 4.2.2 "use of automated decision making (ADM)" covering underwriting, pricing, claims triage. Only the "effect on the individual" element is thin. NOT a clean prospect. (privacy@guildgroup.com.au seen on site.)
- **nib** — https://www.nib.com.au/legal/privacy-policy — already discloses "rights relating to automated decision making... including profiling". (privacyofficer@nib.com.au on site.)
- **Zurich Australia** — https://www.zurich.com.au/important-information/privacy — full AI section: explains logic, fairness testing, human review on request. (privacy.officer@zurich.com.au on site.)
- **Superhero** — https://www.superhero.com.au/privacy-policy/ — no ADM language at all, but it's a superannuation platform; their policy is thin. hello@superhero.com.au seen. Possible 7th lead if you want a non-insurer.
- **Real Insurance / Covermore** — https://www.realinsurance.com.au/privacy-collection — no ADM language, but it's motor/home, not health. privacy@greenstone.com.au is the administrator's, not theirs.

## Verification notes
- All fetches used a Chrome User-Agent, SSL verification disabled for timeout tolerance.
- No email on this list was constructed or pattern-guessed. NOT_FOUND used where the company publishes no email.
- Browser fallback for Bupa failed (Chromium unavailable in this environment) — Bupa's entry is the weakest of the six; verify manually before emailing.
