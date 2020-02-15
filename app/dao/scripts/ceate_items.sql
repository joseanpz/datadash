CREATE TABLE datadash.items (
    id                SERIAL PRIMARY KEY,
    title             VARCHAR(100),
    description       TEXT,
    owner_id          INTEGER REFERENCES users (id)
);