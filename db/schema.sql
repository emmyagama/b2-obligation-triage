PRAGMA foreign_keys = ON;
CREATE TABLE corpus_documents (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, contract_family TEXT,
  source_url TEXT, char_count INTEGER, page_count INTEGER,
  license TEXT NOT NULL DEFAULT 'CC BY 4.0'
);

CREATE TABLE clause_labels (                -- CUAD's expert labels, ingested verbatim
  id INTEGER PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES corpus_documents(id),
  category TEXT NOT NULL,                   -- one of the 41
  answer_text TEXT, char_start INTEGER, char_end INTEGER,
  UNIQUE (document_id, category, char_start, char_end)
);

CREATE TABLE obligation_types (
  code TEXT PRIMARY KEY,                    -- 'NOTICE_PERIOD_RENEWAL', ...
  name TEXT NOT NULL,
  cuad_category TEXT,                       -- maps to clause_labels.category
  deadline_behaviour TEXT NOT NULL
    CHECK (deadline_behaviour IN ('absolute','relative','recurring','none')),
  escalates_by_default INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE intakes (
  id INTEGER PRIMARY KEY,
  external_ref TEXT UNIQUE NOT NULL,        -- idempotency at the boundary
  document_id TEXT NOT NULL REFERENCES corpus_documents(id),
  intake_party TEXT NOT NULL
    CHECK (intake_party IN ('provider','customer','licensee','licensor','other')),
  business_context TEXT, channel TEXT NOT NULL, received_at TEXT NOT NULL
);

CREATE TABLE runs (
  id INTEGER PRIMARY KEY,
  intake_id INTEGER NOT NULL REFERENCES intakes(id),
  model TEXT NOT NULL, prompt_version TEXT NOT NULL,
  schema_version TEXT NOT NULL, corpus_version TEXT NOT NULL,
  started_at TEXT, finished_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('ok','escalated','failed')),
  latency_ms INTEGER, tokens_in INTEGER, tokens_out INTEGER, cost_usd REAL,
  cache_hit INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE tool_calls (
  id INTEGER PRIMARY KEY,
  run_id INTEGER NOT NULL REFERENCES runs(id), seq INTEGER NOT NULL,
  tool_name TEXT NOT NULL, args_json TEXT, result_json TEXT,
  latency_ms INTEGER, retry_count INTEGER NOT NULL DEFAULT 0,
  error_class TEXT, cache_hit INTEGER NOT NULL DEFAULT 0,
  UNIQUE (run_id, seq)
);

CREATE TABLE decisions (
  id INTEGER PRIMARY KEY,
  run_id INTEGER NOT NULL UNIQUE REFERENCES runs(id),  -- one terminal decision per run
  obligation_count INTEGER NOT NULL DEFAULT 0,
  confidence REAL CHECK (confidence BETWEEN 0 AND 1),
  escalated INTEGER NOT NULL DEFAULT 0,
  escalation_codes_json TEXT
);

CREATE TABLE obligations (
  id INTEGER PRIMARY KEY,
  decision_id INTEGER NOT NULL REFERENCES decisions(id),
  obligation_type TEXT NOT NULL REFERENCES obligation_types(code),
  description TEXT NOT NULL,
  owed_by TEXT NOT NULL CHECK (owed_by IN ('provider','customer','both','unclear')),
  clause_category TEXT NOT NULL,
  clause_quote TEXT NOT NULL,               -- verbatim, never paraphrased
  consequence TEXT,
  confidence REAL CHECK (confidence BETWEEN 0 AND 1),
  needs_human INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE obligation_deadlines (
  id INTEGER PRIMARY KEY,
  obligation_id INTEGER NOT NULL REFERENCES obligations(id),
  deadline_kind TEXT NOT NULL
    CHECK (deadline_kind IN ('absolute','relative','recurring','none')),
  raw_text TEXT,                            -- verbatim; never normalised away
  resolved_date TEXT,                       -- ISO date when computable
  anchor_event TEXT, offset_days INTEGER,   -- for relative deadlines
  recurring_rule TEXT,
  CHECK (deadline_kind <> 'absolute' OR resolved_date IS NOT NULL)
);

CREATE TABLE escalations (
  id INTEGER PRIMARY KEY,
  decision_id INTEGER NOT NULL REFERENCES decisions(id),
  reason_code TEXT NOT NULL,
  queue TEXT NOT NULL CHECK (queue IN ('legal-ops','engineering')),
  created_at TEXT NOT NULL, resolved_at TEXT,
  human_obligation_count INTEGER
);

CREATE TABLE human_reviews (                -- the real-humans loop
  id INTEGER PRIMARY KEY,
  escalation_id INTEGER NOT NULL REFERENCES escalations(id),
  reviewer_id TEXT NOT NULL, reviewer_role TEXT NOT NULL,
  verdict TEXT NOT NULL
    CHECK (verdict IN ('agree','disagree','insufficient_information')),
  note TEXT, reviewed_at TEXT NOT NULL,
  UNIQUE (escalation_id, reviewer_id)
);

CREATE TABLE idempotency (
  key TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
  run_id INTEGER, created_at TEXT NOT NULL
);

CREATE TABLE dead_letter (
  id INTEGER PRIMARY KEY, run_id INTEGER,
  error_class TEXT NOT NULL, error_detail TEXT,
  payload_json TEXT, created_at TEXT NOT NULL
);
