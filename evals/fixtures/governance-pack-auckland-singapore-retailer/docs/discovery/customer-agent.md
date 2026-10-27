# Discovery brief: customer service at Kowhai Retail

Status: accepted 2026-08-19 by Mere Walker (General Manager, Customer)
Prepared by: Southgate Labs, Sydney

## 1. Context

Kowhai Retail Limited (Auckland, New Zealand) runs 41 stores in New Zealand and, through
Kowhai Retail (Singapore) Pte. Ltd., 9 stores in Singapore, plus online shops in both
countries. Customer service handles 22,000 enquiries a month in Auckland and Singapore.

## 2. First workflow and outcome

- **Workflow:** "where is my order", returns and refunds-as-store-credit enquiries in web chat.
- **Outcome measure:** enquiries resolved in chat without an agent (chat platform).
- **Baseline:** 18 % (July 2026, FAQ bot).
- **Counter-metric:** store credit issued per 1,000 chats; baseline 31 (agents only).
- **Decider:** Mere Walker.

## 3. Data register

| Data | Subjects | Source | Notes |
| --- | --- | --- | --- |
| Customer profile and order history (name, email, phone, address, orders, returns) | customers in New Zealand and Singapore | Salesforce CRM (read) | collected by Kowhai through its shops and loyalty programme |
| Store credit ledger | customers | Salesforce CRM (write: issue credit) | |
| Chat transcripts | customers | the agent | kept and reused to build evaluation sets |

## 4. Harms and cost of a wrong answer

- Credit issued to the wrong customer or above policy costs money and may disclose an order.
- A wrong delivery or returns answer misleads a customer.
- Old or wrong CRM data (an outdated address) leads to a wrong answer.

## 5. Stakeholders

- Sponsor and decider: Mere Walker.
- Privacy officer (NZ): Aroha Ngata. Data Protection Officer (Singapore): Daniel Tan.
- Southgate Labs: Priya Raman (engagement lead), three engineers in Sydney.

## 6. Decision calendar

Pilot decision: 2026-11-26. Pilot: web chat for signed-in customers in both countries, 6 weeks.
