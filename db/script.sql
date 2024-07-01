CREATE DATABASE IF NOT EXISTS urldb;

USE urldb;

CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_url VARCHAR(255) NOT NULL,
    UNIQUE KEY idx_short_url (short_url)
);

