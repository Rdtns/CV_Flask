DROP TABLE IF EXISTS Clients;

CREATE TABLE Clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    auteur TEXT NOT NULL
);
