
CREATE TABLE org_credential (
    id BIGINT PRIMARY KEY,
    category TEXT NOT NULL,
    issuer TEXT NOT NULL,
    issuer_url TEXT,
    credential_type TEXT NOT NULL UNIQUE,
    display TEXT NOT NULL,
    credential_url TEXT
);

CREATE INDEX org_credential_category_idx ON org_credential(category);
CREATE INDEX org_credential_issuer_idx ON org_credential(issuer);