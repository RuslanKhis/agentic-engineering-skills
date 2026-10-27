# Request from Priya (support lead), 2026-10-25

Every production session lands in `support_analytics.agent_events`. I'd like a
nightly job that scores yesterday's sessions with Google's BigQuery Agent
Analytics SDK and stops the next release if they fail. And once a month: how
much of real traffic do our 40 golden questions still cover, and which of them
have stopped telling us anything?
