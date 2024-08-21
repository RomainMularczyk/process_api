CREATE DATABASE process_monitoring;

CREATE TABLE process_usage (
    id SERIAL PRIMARY KEY,
    process VARCHAR(255) NOT NULL,
    user VARCHAR(255) NOT NULL,
    cpu FLOAT NOT NULL,
    memory FLOAT NOT NULL,
    command TEXT NOT NULL,
    time TIMESTAMP NOT NULL
);
