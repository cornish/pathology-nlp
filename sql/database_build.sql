-- do we need to track if something is for bladder vs prostate?
-- unit standardization/concept?

create or replace table concept(
  concept_id INTEGER PRIMARY KEY AUTOINCREMENT,
  concept TEXT NOT NULL
  parent_id INTEGER,
  data_type TEXT NOT NULL,
  repeatable BOOLEAN,
  start_date DATE,
  end_date DATE
);

create or replace table concept_alias(
  concept_id INTEGER PRIMARY KEY,
  alias TEXT NOT NULL
);

create or replace table concept_terminology_mapping (
  concept_id INTEGER NOT NULL,
  external_terminology TEXT NOT NULL,
  external_id TEXT NOT NULL
);

reate or replace table domain_id(
  domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT NOT NULL,
  uri TEXT NOT NULL,
  start_date DATE,
  end_date DATE
);

create or replace table concept_domain_mapping (
  concept_id INTEGER NOT NULL,
  domain_id INTEGER NOT NULL
);

create or replace table original_report(
  case_id TEXT NOT NULL,
  parts TEXT NOT NULL,
  diagnosticcomment TEXT NOT NULL,
  finaldiagnosis TEXT NOT NULL,
  microscopicdescription TEXT NOT NULL,
  PRIMARY KEY (case_id)
);

create or replace table structured_report (
  case_id TEXT NOT NULL,
  concept_id NOT NULL,
  concept_value NOT NULL,
  PRIMARY KEY (case_id)
);