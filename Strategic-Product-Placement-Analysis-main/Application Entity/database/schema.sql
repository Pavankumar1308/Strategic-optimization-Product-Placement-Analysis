-- Strategic Product Placement Analysis - Database Schema (MySQL)
CREATE DATABASE IF NOT EXISTS sppa_db;
USE sppa_db;

-- Users table (authentication)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','manager','analyst') DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_code INT NOT NULL,
    product_category ENUM('Clothing','Electronics','Food') NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    competitor_price DECIMAL(8,2) NOT NULL
);

-- Placement / Sales records table (core dataset)
CREATE TABLE IF NOT EXISTS sales_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_position ENUM('Aisle','End-cap','Front of Store') NOT NULL,
    promotion ENUM('Yes','No') NOT NULL,
    foot_traffic ENUM('Low','Medium','High') NOT NULL,
    consumer_demographic ENUM('Young adults','College students','Families','Seniors') NOT NULL,
    seasonal ENUM('Yes','No') NOT NULL,
    sales_volume INT NOT NULL,
    record_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ML Predictions log
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_category VARCHAR(50),
    product_position VARCHAR(50),
    promotion VARCHAR(10),
    foot_traffic VARCHAR(20),
    seasonal VARCHAR(10),
    predicted_sales_volume DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_sales_category ON sales_records(product_id);
CREATE INDEX idx_sales_position ON sales_records(product_position);
