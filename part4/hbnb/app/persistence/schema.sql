-- Disable FOREIGN_KEY_CHECKS to allow for clean drop of the tables
SET FOREIGN_KEY_CHECKS = 0;
DROP  TABLE IF EXISTS User;
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS Review;
SET FOREIGN_KEY_CHECKS = 1;

-- User table creation
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Place table creation
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Review table creation
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 TO 5),
    user_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCING User(id) ON DELETE CASCADE,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (place_id) REFERENCING Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- Amenity table creation
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Place_Amenity table creation
CREATE TABLE Place_Amenity (
    place_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCING Place(id) ON DELETE CASCADE,
    amenity_id CHAR(36) NOT NULL,
    FOREIGN KEY (amenity_id) REFERENCING Amenity(id) ON DELETE CASCADE
);
