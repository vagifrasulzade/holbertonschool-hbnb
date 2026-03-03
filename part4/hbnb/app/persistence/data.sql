-- Insert Administrator
INSERT INTO User (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQv3c1yqBWVHxkd0LpUuoe6Wysyz6zvnW9T8atB9YI7i/F3OQ8ZSy',
    TRUE
);

-- Insert Amenities
INSERT INTO Amenity name VALUES
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning');