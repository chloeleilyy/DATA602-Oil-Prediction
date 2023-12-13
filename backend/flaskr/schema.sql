DROP TABLE IF EXISTS oil_price;

CREATE TABLE oil_price (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  oil_price FLOAT DEFAULT null,
  prediction FLOAT DEFAULT null
);

