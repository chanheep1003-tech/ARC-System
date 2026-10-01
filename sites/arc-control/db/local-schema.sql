-- Development bootstrap only. Production migrations must be generated with Drizzle.
CREATE TABLE IF NOT EXISTS arc_records (
 id TEXT PRIMARY KEY NOT NULL,
 kind TEXT NOT NULL,
 title TEXT NOT NULL,
 payload TEXT NOT NULL,
 revision INTEGER DEFAULT 1 NOT NULL,
 updated_at TEXT NOT NULL
);
