USE hbnb_db;

SELECT * FROM user WHERE is_admin = TRUE;

INSERT INTO place (id, title, description, price, latitude, longitude, owner_id) VALUES (
    UUID(),
    'Yougiboubi',
    'Je sais pas quoi mettre',
    299.99,
    25.7617,
    -80.1918,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

INSERT INTO place_amenity (place_id, amenity_id) SELECT
    (SELECT id FROM place WHERE title = 'Yougiboubi'),
    (SELECT id FROM amenity WHERE name = 'WiFi');

UPDATE place SET price = 319.99 WHERE title = 'Yougiboubi';

DELETE FROM place WHERE title = 'Yougiboubi';