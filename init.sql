-- This script runs when the database container is initialized for the first time.
-- It is mounted to /docker-entrypoint-initdb.d/init.sql in docker-compose.yml.

-- You can add SQL commands here to seed the database with initial data.
-- Note: The database (library_db) and user (postgres) are created by environment variables in docker-compose.yml.

-- Example:
-- CREATE TABLE IF NOT EXISTS example (id SERIAL PRIMARY KEY, name TEXT);
-- INSERT INTO example (name) VALUES ('Initial Data');
