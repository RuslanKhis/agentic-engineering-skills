# Discovery brief: staff HR assistant at Wattle & Co

Status: accepted 2026-09-10 by Marcus Bell (Chief People Officer)
Prepared by: Southgate Labs, Sydney

## 1. Context

Wattle & Co Pty Ltd is an Australian homewares retailer with 4,800 staff across 96 stores and
a support office in Sydney: 2,100 in NSW, 1,600 in Victoria and 1,100 in Queensland. Staff use
Workday for leave, rosters and time and attendance. The HR service centre answers about 3,900
staff questions a month.

## 2. First workflow and outcome

- **Workflow:** staff questions about leave balances, rosters and HR policy; managers' questions
  about their team's leave and attendance.
- **Outcome measure:** HR service centre tickets per month (service desk report).
- **Baseline:** 3,900 tickets a month (June to August 2026).
- **Counter-metric:** share of answers staff mark as wrong; target under 5 %.
- **Decider:** Marcus Bell.

## 3. Data register

| Data | Subjects | Source | Notes |
| --- | --- | --- | --- |
| Leave balances and leave history (including personal/carer's leave reasons where staff typed them) | employees in NSW, VIC, QLD | Workday leave API (read) | free-text reasons may mention illness, family or union matters |
| Rosters | employees | Workday scheduling API (read) | |
| Time and attendance (clock-in, lateness, absences) | employees | Workday time API (read) | managers see their team |
| Chat prompts and answers | employees and managers | the assistant | logged |

## 4. Harms and cost of a wrong answer

- A wrong leave balance leads a staff member to book leave they do not have.
- A manager's attendance summary may be used in a performance conversation; a wrong or
  context-free summary can affect someone's employment.
- Prompts can contain health, family or union information.

## 5. Stakeholders

- Sponsor and decider: Marcus Bell, Chief People Officer.
- Privacy Officer: Grace Nguyen. Head of Security: Daniel Okoro.
- Employee relations: Shop, Distributive and Allied Employees' Association (SDA) delegates
  in the stores; the enterprise agreement requires consultation on major workplace change.
- Southgate Labs: Priya Raman (engagement lead), three engineers in Sydney.

## 6. Decision calendar

Pilot decision: 2026-11-27, people leadership meeting. Pilot: 300 staff and 25 managers in
NSW stores.
