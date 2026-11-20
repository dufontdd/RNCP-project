-- ---------------------------------------------------
-- Manhwa Project: Database Schema
-- File: schema.sql
-- ---------------------------------------------------

DROP TABLE IF EXISTS manhwa_genre;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS manhwas;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS users;

-- ---------------- USERS ----------------
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);

-- ---------------- GENRES ----------------
CREATE TABLE genres (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

-- ---------------- MANHWAS ----------------
CREATE TABLE manhwas (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

-- ---------------- REVIEWS ----------------
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    user_id TEXT NOT NULL,
    manhwa_id TEXT NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(manhwa_id) REFERENCES manhwas(id)
);

-- ---------------- MANHWA_GENRE ----------------
CREATE TABLE manhwa_genre (
    manhwa_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    PRIMARY KEY (manhwa_id, genre_id),
    FOREIGN KEY(manhwa_id) REFERENCES manhwas(id),
    FOREIGN KEY(genre_id) REFERENCES genres(id)
);
