DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    created_at NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (data) VALUES 
    ("{0}"),
    ("{1}"),
    ("{2}"),
    ("{3}");