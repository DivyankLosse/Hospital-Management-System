-- Create Database
CREATE DATABASE hms;
\c hms;

-- Users table (For authentication)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table (Replaces 'guests')
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100),
    email VARCHAR(50) UNIQUE NOT NULL,
    phone BIGINT NOT NULL UNIQUE,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Login table (For additional security questions)
CREATE TABLE login (
    username VARCHAR(50) PRIMARY KEY,
    password TEXT NOT NULL,
    sec_que TEXT,
    sec_ans TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table (Replaces reservations)
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled', -- Options: Scheduled, Completed, Canceled
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Sample Data Insertions (Optional)
INSERT INTO users (email, password, name) VALUES
('john@doe.com', 'hashed_password_123', 'John Doe');

INSERT INTO patients (name, address, email, phone, city) VALUES
('John Doe', 'US', 'john@doe.com', 1231231231, 'NYC');

INSERT INTO appointments (patient_id, appointment_date, status, notes) VALUES
(1, '2025-02-05 10:30:00', 'Scheduled', 'Routine checkup');
