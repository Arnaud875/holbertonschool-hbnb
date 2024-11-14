CREATE DATABASE IF NOT EXISTS hbnb_db;
USE hbnb_db;

DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id VARCHAR(36) PRIMARY KEY,

    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE place (
    id VARCHAR(36) PRIMARY KEY,

    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id VARCHAR(36) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE CASCADE,
    CHECK (price >= 0),
    CHECK (latitude BETWEEN -90 AND 90),
    CHECK (longitude BETWEEN -180 AND 180)
);

CREATE TABLE review (
    id VARCHAR(36) PRIMARY KEY,

    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    place_id VARCHAR(36) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id),
    CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE amenity (
    id VARCHAR(36) PRIMARY KEY,

    name VARCHAR(255) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
);

INSERT INTO user (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NNbQ4P5Ei',
    TRUE
);

INSERT INTO amenity (id, name) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi'),
    ('550e8400-e29b-41d4-a716-446655440001', 'Swimming Pool'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Air Conditioning');