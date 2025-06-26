CREATE DATABASE library;

USE library;

CREATE TABLE members (
	member_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    member_password VARCHAR(150) NOT NULL,
    member_type ENUM('student', 'lecturer') DEFAULT 'student'
);

CREATE TABLE books (
	book_id INT PRIMARY KEY AUTO_INCREMENT,
    book_title VARCHAR(100),
    author VARCHAR(150),
    ISBN VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(100),
    book_description TEXT,
    available_copies INT DEFAULT 1
);

CREATE TABLE issues (
	issue_id INT PRIMARY KEY,
    book_id INT,
    member_id INT,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY(book_id) REFERENCES books(book_id),
    FOREIGN KEY(member_id) REFERENCES members(member_id)
);