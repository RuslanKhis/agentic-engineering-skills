# Discovery brief: customer service assistant at Thamesbridge

Status: accepted 2026-08-28 by Laura Whitfield (Director of Customer Operations)
Prepared by: Southgate Labs, Sydney

## 1. Context

Thamesbridge Bank plc is a UK retail bank (FCA and PRA regulated). Thamesbridge Bank Ireland
DAC, its subsidiary, is regulated by the Central Bank of Ireland and serves customers in
Ireland, with some customers resident elsewhere in the EU. The contact centres in Leeds and
Cork take 610,000 chats and calls a month.

## 2. First workflow and outcome

- **Workflow:** balance and transaction questions, card freezes, and "why was my overdraft
  request declined?" questions in app chat.
- **Outcome measure:** share of chats resolved without transfer to an agent (chat platform).
- **Baseline:** 22 % (July 2026, existing menu bot).
- **Counter-metric:** complaints mentioning the chat, per 10,000 chats (complaints system);
  baseline 3.1.
- **Decider:** Laura Whitfield.

## 3. Data register

| Data | Subjects | Source | Notes |
| --- | --- | --- | --- |
| Account balances and transactions | customers in the UK, Ireland and other EU countries | core banking API (read) | transactions reveal health, religion and union payments in merchant names |
| Card status | customers | card platform API (freeze only) | |
| Overdraft decision and reason codes | customers who applied | credit decision engine (read) | decisions are made by the decision engine, not the assistant |
| Chat transcripts | customers | the assistant | pseudonymised copies kept for support |

## 4. Harms and cost of a wrong answer

- A wrong explanation of a declined overdraft misleads a customer about their credit.
- A card frozen in error stops a customer paying; a freeze not made leaves fraud running.
- A balance from the wrong account discloses another customer's data.

## 5. Stakeholders

- Sponsor and decider: Laura Whitfield. UK DPO: Oliver Grant. Ireland DPO: Siobhán Kelly.
  Group CISO: Rachel Adeyemi. Consumer Duty champion: board member Ian Shah.
- Southgate Labs: Priya Raman (engagement lead), four engineers in Sydney.

## 6. Decision calendar

Pilot decision: 2026-12-03, Customer Operations Committee. Pilot: 5,000 UK and 1,000 Irish
customers who opt in.
