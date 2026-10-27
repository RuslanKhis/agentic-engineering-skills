# Discovery brief: public enquiries at the NSW Trades Licensing Office

Status: accepted 2026-08-26 by Ruth Abbott (Deputy Commissioner, Customer and Licensing)
Prepared by: Southgate Labs, Sydney

## 1. Context

The NSW Trades Licensing Office is a NSW Government executive agency. Its contact centre in
Parramatta answers about 48,000 calls and web enquiries a month, mostly "how do I apply",
"what does this licence class allow" and "where is my application".

## 2. First workflow and outcome

- **Workflow:** public web chat enquiries on the Office's website.
- **Outcome measure:** contact-centre calls per month about application status (telephony
  report).
- **Baseline:** 17,500 calls a month (May to July 2026).
- **Counter-metric:** complaints about wrong or misleading information, per month; baseline 14.
- **Decider:** Ruth Abbott.

## 3. Data register

| Data | Subjects | Source | Notes |
| --- | --- | --- | --- |
| Published guidance pages | none | the Office's website | |
| Application status (application number, stage, missing documents) | applicants for trade licences in NSW | licensing system API (read) | looked up after the caller gives the application number and date of birth |
| Chat transcripts | members of the public | the assistant | may hold names, addresses, health and criminal-history disclosures typed by callers |

## 4. Harms and cost of a wrong answer

- Wrong guidance about what a licence allows can lead to unlicensed work.
- A status lookup for the wrong application discloses another person's information.

## 5. Stakeholders

- Sponsor and decider: Ruth Abbott, who is also the agency's Accountable Official for AI.
- Privacy officer: Sam Taylor. CISO: Nikhil Rao. Records manager: Fiona Lee.
- Southgate Labs: Priya Raman (engagement lead), two engineers in Sydney, one support
  engineer in Brisbane.

## 6. Decision calendar

Pilot decision: 2026-12-10, executive board. Pilot: chat on the "Apply for a licence" pages
for six weeks.
