create table users
(
    id serial primary key,
    username text not null,
    password text not null,
    mail text,
    role text
);

create table books
(
    isbn text primary key,
    name text,
    author text,
    year int
);

create table authors
(
    id serial primary key,
    name text,
    book text[]
);

create table personel(
    id serial primary key,
    username text,
    password text,
    mail text,
    role text
);