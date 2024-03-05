DROP TABLE IF EXISTS Clients;

CREATE TABLE Clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    father_name TEXT NOT NULL,
    mother_name TEXT NOT NULL,
    permanent_address NOT NULL    
);
