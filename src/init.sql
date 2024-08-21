CREATE DATABASE process_monitoring;

CREATE TABLE process_usage (
    id SERIAL PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    cpu FLOAT NOT NULL,
    memory FLOAT NOT NULL,
    command VARCHAR(255) NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE INDEX idx_command ON process_usage(command);
