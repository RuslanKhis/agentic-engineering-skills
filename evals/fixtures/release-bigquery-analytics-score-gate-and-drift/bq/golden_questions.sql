-- Reviewed questions with the answer a support lead approved.
CREATE TABLE IF NOT EXISTS support_analytics.golden_questions (
  question_id STRING NOT NULL,
  question STRING NOT NULL,
  approved_answer STRING NOT NULL,
  topic STRING,
  reviewed_by STRING,
  reviewed_on DATE
);
