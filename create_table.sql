CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE channels (
    id INTEGER PRIMARY KEY,
    link TEXT NOT NULL,
    category TEXT REFERENCES categories(name)
)

