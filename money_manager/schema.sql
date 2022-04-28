DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS movements CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS countries CASCADE;

CREATE TABLE accounts (
    id SERIAL,
    name TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE categories (
    id SERIAL,
    category TEXT UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE countries (
    id SERIAL,
    country TEXT UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id SERIAL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    FirstName TEXT NOT NULL,
    LastNAme TEXT NOT NULL,
    birth DATE NOT NULL,
    country INTEGER NOT NULL,
    password TEXT NOT NULL, 
    PRIMARY KEY (id),
    CONSTRAINT fk_country
        FOREIGN KEY (country) 
            REFERENCES countries(id)
);

CREATE TABLE movements (
    id SERIAL,
    user_id INTEGER,
    account_id INTEGER,
    mov_date TIMESTAMP,
    amount FLOAT,
    category_id INTEGER,
    PRIMARY KEY (id),
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users(id),
    CONSTRAINT fk_account
        FOREIGN KEY (account_id)
            REFERENCES accounts(id), 
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
            REFERENCES categories(id)
);

