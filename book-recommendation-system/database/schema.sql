CREATE DATABASE IF NOT EXISTS book_recommendation;

USE book_recommendation;

CREATE TABLE IF NOT EXISTS books {
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    description TEXT,
    genres TEXT,
    avg_rating DOUBLE,
    num_ratings BIGINT,
    url VARCHAR(255)
};
