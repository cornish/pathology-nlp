-- do we need to track if something is for bladder vs prostate?
-- unit standardization/concept?

DROP TABLE IF EXISTS concept;
CREATE TABLE concept(
  concept_id INTEGER PRIMARY KEY AUTOINCREMENT,
  concept TEXT NOT NULL,
  parent_id INTEGER,
  data_type TEXT,
  repeatable BOOLEAN,
  start_date DATE,
  end_date DATE
);

DROP TABLE IF EXISTS concept_alias;
CREATE TABLE concept_alias(
  concept_id INTEGER PRIMARY KEY,
  alias TEXT NOT NULL,
  FOREIGN KEY(concept_id) REFERENCES concept(concept_id)
);

DROP TABLE IF EXISTS concept_terminology_mapping;
CREATE TABLE concept_terminology_mapping (
  concept_id INTEGER NOT NULL,
  external_terminology TEXT NOT NULL,
  external_id TEXT NOT NULL,
  FOREIGN KEY(concept_id) REFERENCES concept(concept_id)
);

DROP TABLE IF EXISTS domain;
CREATE TABLE domain(
  domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT NOT NULL,
  uri TEXT NOT NULL,
  start_date DATE,
  end_date DATE
);

DROP TABLE IF EXISTS concept_domain_mapping;
CREATE TABLE concept_domain_mapping (
  concept_id INTEGER NOT NULL,
  domain_id INTEGER NOT NULL,
  FOREIGN KEY(concept_id) REFERENCES concept(concept_id),
  FOREIGN KEY(domain_id) REFERENCES domain(domain_id)
);

DROP TABLE IF EXISTS original_report;
CREATE TABLE original_report(
  case_id TEXT NOT NULL,
  parts TEXT NOT NULL,
  diagnosticcomment TEXT NOT NULL,
  finaldiagnosis TEXT NOT NULL,
  microscopicdescription TEXT NOT NULL,
  PRIMARY KEY (case_id)
);

DROP TABLE IF EXISTS structured_report;
CREATE TABLE structured_report (
  case_id TEXT NOT NULL PRIMARY KEY,
  concept_id NOT NULL,
  concept_value NOT NULL,
  FOREIGN KEY(case_id) REFERENCES original_report(case_id),
  FOREIGN KEY(concept_id) REFERENCES concept(concept_id)
);
