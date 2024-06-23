CREATE TABLE IF NOT EXISTS navMenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS pizza (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
description text NOT NULL,
price integer NOT NULL,
photo BLUB DEFAULT NULL
);