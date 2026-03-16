
CREATE TABLE IF NOT EXISTS dctnry.org_credential (
    id BIGINT PRIMARY KEY,
    category TEXT NOT NULL,
    issuer TEXT NOT NULL,
    issuer_url TEXT,
    credential_type TEXT NOT NULL UNIQUE,
    display TEXT NOT NULL,
    credential_url TEXT,
    is_credential_retired BOOLEAN NOT NULL DEFAULT FALSE,
    is_cms_deeming_credential BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

CREATE INDEX org_credential_category_idx ON dctnry.org_credential(category);
CREATE INDEX org_credential_issuer_idx ON dctnry.org_credential(issuer);