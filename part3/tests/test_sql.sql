CREATE TABLE IF NOT EXISTS Users (
    id VARCHAR(38) PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Amenities (
    id VARCHAR(38) PRIMARY KEY,

    name VARCHAR(50) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Reviews (
    id VARCHAR(38) PRIMARY KEY,

    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    place_id VARCHAR(38) NOT NULL,
    user_id VARCHAR(38) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Places(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Places (
    id VARCHAR(38) PRIMARY KEY,

    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id VARCHAR(38) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS place_amenities (
    place_id VARCHAR(38) NOT NULL,
    amenity_id VARCHAR(38) NOT NULL,

    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Places(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenities(id)
);

-- Exemple d'insertion dans la table Users
INSERT INTO Users (id, email, first_name, last_name, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQvX5HLRuNv8pDQ3iCw5hOYQ5ABJZ9.QS',
    1
);

-- Exemple d'insertion dans la table Amenities
INSERT INTO Amenities (id, name) VALUES
    ('b5f9d7d1-5c9c-4c7f-9b6d-8e4a9b2f5e1a', 'WiFi'),
    ('c6e8f3a2-6d8b-4d9e-8c7f-9a1b2c3d4e5f', 'Swimming Pool'),
    ('d7f9e3b2-7c8a-4b9d-9e8f-8d7c6b5a4e3d', 'Air Conditioning');
