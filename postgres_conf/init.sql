CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE incidentdb OWNER myuser;

\c incidentdb

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    caller_name VARCHAR(100),
    caller_email VARCHAR(100),
    subject VARCHAR(200),
    description TEXT,
    status VARCHAR(50),
    priority VARCHAR(20),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO incidents (caller_name, caller_email, subject, description, status, priority, category) VALUES
    ('John Doe', 'john.doe@example.com', 'Cannot access email', 'I am unable to log into my email account since this morning.', 'Open', 'Medium', 'Email'),
    ('Jane Smith', 'jane.smith@example.com', 'Printer not working', 'The printer on the 2nd floor is not responding to print jobs.', 'In Progress', 'Low', 'Hardware'),
    ('Mike Johnson', 'mike.johnson@example.com', 'VPN connection issues', 'I cannot establish a VPN connection from my home office.', 'Open', 'High', 'Network'),
    ('Sarah Brown', 'sarah.brown@example.com', 'Software license expired', 'My design software license has expired and I need it renewed.', 'Closed', 'Medium', 'Software'),
    ('Tom Wilson', 'tom.wilson@example.com', 'New laptop request', 'I need a new laptop for my upcoming project starting next week.', 'Open', 'Low', 'Hardware');
