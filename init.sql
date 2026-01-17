-- This script runs when the database container is initialized for the first time.
-- It is mounted to /docker-entrypoint-initdb.d/init.sql in docker-compose.yml.

-- Create tables if they don't exist (to support running before migrations)

CREATE TABLE IF NOT EXISTS library_location (
    id BIGSERIAL PRIMARY KEY,
    slug VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS library_author (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Note: library_book table definition must match Django's schema
CREATE TABLE IF NOT EXISTS library_book (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) NOT NULL UNIQUE,
    pages INTEGER NOT NULL,
    nfc_tag VARCHAR(255) UNIQUE,
    book_type VARCHAR(20) NOT NULL DEFAULT 'fantasy',
    genre VARCHAR(100),
    location_id BIGINT REFERENCES library_location(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED,
    author_id BIGINT REFERENCES library_author(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- Indexes (simplified)
CREATE INDEX IF NOT EXISTS library_book_location_id_idx ON library_book(location_id);
CREATE INDEX IF NOT EXISTS library_book_author_id_idx ON library_book(author_id);
CREATE INDEX IF NOT EXISTS library_location_slug_idx ON library_location(slug);

-- Data Seeding

-- Locations
INSERT INTO library_location (id, slug, display_name, description) VALUES
(1, 'shelf-a1', 'Shelf A1', 'Fantasy Section - Aisle A'),
(2, 'shelf-a2', 'Shelf A2', 'Science Fiction Section - Aisle A'),
(3, 'shelf-b1', 'Shelf B1', 'Classic Literature - Aisle B'),
(4, 'shelf-b2', 'Shelf B2', 'Mystery & Thrillers - Aisle B')
ON CONFLICT (id) DO NOTHING;

-- Authors
INSERT INTO library_author (id, name) VALUES
(1, 'J.K. Rowling'),
(2, 'J.R.R. Tolkien'),
(3, 'Isaac Asimov'),
(4, 'Frank Herbert'),
(5, 'Jane Austen'),
(6, 'Arthur Conan Doyle')
ON CONFLICT (id) DO NOTHING;

-- Books
INSERT INTO library_book (id, name, isbn, pages, nfc_tag, book_type, genre, location_id, author_id) VALUES
(1, 'Harry Potter and the Sorcerer''s Stone', '9780590353427', 309, 'NFC001', 'fantasy', 'Magic', 1, 1),
(2, 'The Hobbit', '9780547928227', 310, 'NFC002', 'fantasy', 'Adventure', 1, 2),
(3, 'Foundation', '9780553293357', 255, 'NFC003', 'science', 'Space Opera', 2, 3),
(4, 'Dune', '9780441172719', 412, 'NFC004', 'science', 'Epic', 2, 4),
(5, 'Pride and Prejudice', '9780141439518', 279, 'NFC005', 'romance', 'Classic', 3, 5),
(6, 'The Adventures of Sherlock Holmes', '9780140439073', 307, 'NFC006', 'thriller', 'Mystery', 4, 6)
ON CONFLICT (id) DO NOTHING;

-- Reset sequences
SELECT setval('library_location_id_seq', (SELECT MAX(id) FROM library_location));
SELECT setval('library_author_id_seq', (SELECT MAX(id) FROM library_author));
SELECT setval('library_book_id_seq', (SELECT MAX(id) FROM library_book));
