-- Setup mysql server
-- configure persmissions

-- CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
-- GRANT ALL PRIVILEGES ON my_db.* TO 'root'@'localhost';

CREATE DATABASE IF NOT EXISTS my_db;
USE my_db;

DROP TABLE IF EXISTS users;

CREATE TABLE users(
	email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");
