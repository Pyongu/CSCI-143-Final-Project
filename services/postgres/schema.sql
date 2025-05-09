CREATE EXTENSION postgis;

\set ON_ERROR_STOP on

BEGIN;

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

CREATE TABLE users (
    id_users BIGINT UNIQUE,
    username text PRIMARY KEY,
    password text
);

CREATE TABLE tweets (
    id_tweets BIGINT PRIMARY KEY,
    text TEXT,
    created_at TIMESTAMPTZ
);

COMMIT;
