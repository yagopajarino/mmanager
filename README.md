# MM: Harvard's CS50 Final Project

Creación de una aplicación web usando el framework de programación web flask y conexión a base de datos SQL de PostgreSQL. Deployment en Heroku.


<a href="https://moneym.herokuapp.com"><img width="1000" alt="image" src="https://user-images.githubusercontent.com/50267208/165157656-099e1914-2fc4-4c39-852e-486482037d6d.png"></a>

## Diseño

Creación de las pantallas usando HTML, CSS y javaScript.

Register

<img width="813" alt="image" src="https://user-images.githubusercontent.com/50267208/165141063-227f9e58-3b09-45d8-a699-6bbfa75bba73.png">

Login

<img width="813" alt="image" src="https://user-images.githubusercontent.com/50267208/165140992-4c5d71e8-771f-4c0d-877c-b6ab0e738699.png">

Dashboard

<img width="813" alt="image" src="https://user-images.githubusercontent.com/50267208/165140880-4063e40b-1d82-4147-a289-60c8e0264a67.png">

Income/payments

<img width="813" alt="image" src="https://user-images.githubusercontent.com/50267208/165140947-4ba1a6d7-5755-496a-a38f-51c2a9e4dad7.png">

Movements

<img width="813" alt="image" src="https://user-images.githubusercontent.com/50267208/165146157-52533f3e-26d7-4116-a34f-b775f85d2afd.png">

## Data

Conexión a base de datos de [PostgreSQL](https://www.postgresql.org/) utilizando el addOn incluido en [Heroku Postgres - Add-ons](https://elements.heroku.com/addons/heroku-postgresql)

### Schema

Tablas y tipado de datos de la base de datos, determinando primary y foreign keys.
```SQL

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
```
### ERP 

Visualización de tablas, tipo de datos y relaciones.

![image](https://user-images.githubusercontent.com/50267208/165152417-bd9356a9-7a53-47f6-a3a1-2a953dcb8d89.png)

Ver en [dbdiagram](https://dbdiagram.io/d/6266bc5b95e7f23c616b96f9).

### DataClips

Code snippets para acceder a información almacenada en la base de datos para resolver requerimientos de la app y/o obtener información.

#### 1. Movimientos de un usuario

OBJETIVO: Dado un usuario, obtener los datos de fecha, cuenta, categoría y monto de todos los movimientos realizados.

Sea `USUARIO` el username del que queremos obtener todos los movimientos.

```SQL
SELECT movements.Mov_date, accounts.name, categories.category, movements.amount 
FROM movements, users, accounts, categories
WHERE
  movements.user_id = users.id AND
  users.username = USUARIO AND
  accounts.id = movements.account_id AND
  categories.id = movements.category_id;
```
Utilizado para alimentar la pantalla de movements.

#### 2. Movimientos por usuario

OBJETIVO: Obtener la cantidad de movimientos por usuario, ordenado de forma decreciente.

```SQL
SELECT users.username, COUNT(movements.id) FROM movements JOIN users
ON users.id = movements.user_id
GROUP BY users.username
ORDER BY Count DESC
```

#### 3. Cantidad de Usuarios por país

OBJETIVO: Obtener la cantidad de usuarios registrados por país, ordenado de forma decreciente.
```SQL
SELECT countries.country, COUNT(users.id) 
FROM users, countries
WHERE users.country = countries.id
GROUP BY countries.country
ORDER BY Count DESC
```

#### 4. Usuarios menores de 25 años

OBJETIVO: Obtener la cantidad de usuarios registrados menores de 25 años.

```SQL
SELECT count(username) FROM users
WHERE birth + interval '25 year' > CURRENT_DATE;
```




