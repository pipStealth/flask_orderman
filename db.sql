CREATE TABLE IF NOT EXISTS navMenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS food (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
description text NOT NULL,
price integer NOT NULL,
type text DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS account (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL, 
email text NOT NULL,
password text NOT NULL,
phone text NOT NULL,
offer text NOT NULL,
balance integer NOT NULL
);

CREATE TABLE IF NOT EXISTS offer (
id integer PRIMARY KEY AUTOINCREMENT,
foodid text NOT NULL,
phone text NOT NULL, 
adress text NOT NULL
);