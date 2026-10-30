CREATE TABLE IF NOT EXISTS reviews (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source       TEXT        NOT NULL CHECK (source IN ('webhook', 'telegram')),
    article      TEXT,
    rating       SMALLINT    CHECK (rating BETWEEN 1 AND 5),
    review_text  TEXT        NOT NULL CHECK (length(btrim(review_text)) > 0),
    -- Analysis fields stay NULL when status = 'parse_error'.
    sentiment    TEXT        CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    category     TEXT        CHECK (category IN ('size', 'fabric_quality', 'defect', 'delivery', 'not_as_photo', 'other')),
    summary      TEXT,
    needs_reply  BOOLEAN,
    provider     TEXT,
    status       TEXT        NOT NULL DEFAULT 'ok' CHECK (status IN ('ok', 'parse_error')),
    -- Full provider response (valid JSON even when the model text is not).
    raw_response JSONB,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews (created_at);