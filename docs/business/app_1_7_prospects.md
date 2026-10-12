# AU APP 1.7 ADM Disclosure Gaps — Verified Prospects (checked 5 Oct 2026)

APP 1.7 (Privacy Act 1988, from 10 Dec 2026) requires APP entities using automated
decision-making to state in their privacy policy: (a) the purpose of the ADM,
(b) how the ADM is used, (c) the effect on the individual.

METHOD: each policy URL was fetched and full body text keyword-scanned for
"automated", "algorithm", "machine learning", "artificial intelligence",
"decision", "model". All 6 returned ZERO hits for every ADM term, while each
business's own policy text confirms it runs credit assessment/eligibility.

---

## 1. Jacaranda Finance
- Homepage: https://jacarandafinance.com.au/
- Privacy policy: https://jacarandafinance.com.au/about/privacy-policy
- ADM evidence (lending activity): "If you proceed with the credit assessment, we may
  do a hard enquiry on your credit file" / "Based on the information you provide us, we
  can indicate that you qualify for a product... We will then complete an assessment
  and verify the information" — homepage offers instant online eligibility check.
- ADM GAP: zero occurrences of automated/algorithm/machine learning/model/AI in the
  policy. No statement of ADM purpose, use, or effect on individuals. No right to
  explanation, no human-intervention assurance.
- Email: info@jacarandafinance.com.au
  (verified in policy page body as Privacy Officer contact; mailto payload
  base64 "aW5mb0BqYWNhcmFuZGFmaW5hbmNlLmNvbS5hdQ==" on that same page)

## 2. Money3
- Homepage: https://www.money3.com.au/
- Privacy policy: https://www.money3.com.au/privacy-policy/
- ADM evidence: "Assessment is typically completed within 24 to 48 hours once all
  details and bank statements (digitally verified via illion) are provided."
  Credit Licence 389067. Owns the lending decision (not a broker).
- ADM GAP: 0 hits for automated/algorithm/ML/AI/decision model.
- Email: customercare@money3.com.au (homepage + /contact-us/)

## 3. Hume Bank
- Homepage: https://www.humebank.com.au/
- Privacy policy: https://www.humebank.com.au/privacy-policy/
- ADM evidence: "we can do a credit check without asking for your consent" (consumer
  credit) and with consent for commercial credit; credit limit decisions.
  Credit Licence 244248.
- ADM GAP: 0 hits for automated/algorithm/ML/AI/decision.
- Email: hume@humebank.com.au (https://www.humebank.com.au/contact-us/)

## 4. SocietyOne
- Homepage: https://societyone.com.au/
- Privacy policy: https://societyone.com.au/privacypolicy
- ADM evidence: tiered credit-based pricing ("rate advertised ... for a Tier 1
  borrower", "6.99% ... to 24.89%") — automated credit-tier pricing. Credit licence
  no. 423660. Site offers "Get Your Rate" and credit score tool.
- ADM GAP: 0 hits for automated/algorithm/ML/AI/decision.
- Email: s1customer.service@moneyme.com.au
  (NOTE: this is literally the address published in the SocietyOne site footer —
  it points at a MoneyMe domain because MoneyMe operates the platform. Flag to
  buyer; do not present as a societyone.com.au address.)

## 5. Boost Finance
- Homepage: https://www.boostfinance.com.au/
- Privacy policy: https://www.boostfinance.com.au/privacy-policy/
- ADM evidence: "We collect, hold and use Personal Information to: assess and verify
  your identity and your financial situation; assess your consumer or commercial
  credit application... " Credit Licence 386927 / 386930 / 386932.
- ADM GAP: 0 hits for automated/algorithm/ML/AI/decision.
- Email: info@boostfinance.com.au (site footer)

## 6. Automotive Finance
- Homepage: https://www.automotive-finance.com.au/
- Privacy policy: https://www.automotive-finance.com.au/privacy-policy
- ADM evidence: "We use the credit-related information that we exchange with credit
  reporting bodies to confirm your identity, assess your creditworthiness, assess
  your application for finance..." Credit licence 483211.
- ADM GAP: 0 hits for automated/algorithm/ML/AI/decision.
- Email: enquiries@automotive-finance.com.au (https://www.automotive-finance.com.au/contact-us)
  also published: las@automotive-finance.com.au, complaints@..., collections@...

---

## Screened OUT (already disclose ADM — NOT prospects)
- MoneyMe — https://www.moneyme.com.au/privacy-policy — has a full "Automated
  decision-making" section naming credit scoring models, rules engines, ML models,
  and listing solely-automated decisions. Already compliant.
- Azupay — https://azupay.com.au/privacy-policy/ — §1.14 "Automated Decision Making".
- Loan Market — https://www.loanmarket.com.au/consumer-privacy-policy — has
  "Automated Decision Making" section + AI model training disclosure.

## Backups (0 ADM hits, email verified, less credit-decision-owning)
- Nfinance — https://www.nfinance.com.au/privacy-policy/ —
  "We use your Credit-related information to assess your eligibility to be provided
  with finance." Credit Licence 389087. Email on site: tomnightingale@nfinance.com.au
  (personal name, use with care). Also privacy@... NOT verified.
- Lendly — http://www.lendly.com.au/privacy — broker, not decision-maker.
  hello@lendly.com.au