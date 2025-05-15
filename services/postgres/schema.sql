CREATE EXTENSION postgis;

\set ON_ERROR_STOP on

BEGIN;

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE users (
    id_users BIGSERIAL PRIMARY KEY,
    username text UNIQUE,
    password text
);

CREATE TABLE tweets (
    id_tweets BIGSERIAL PRIMARY KEY,
    id_users BIGINT,
    message_text TEXT NOT NULL,
    created_at TIMESTAMPTZ
);

CREATE INDEX on tweets USING btree(created_at, id_users, message_text);

CREATE EXTENSION IF NOT EXISTS rum;
CREATE INDEX on tweets USING RUM(to_tsvector('english', message_text));

COMMIT;
