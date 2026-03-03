erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : is_in

    
    USER {
        char id PK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar password
        boolean is_admin
    }
    PLACE {
        char id PK
        varchar title
        text description
        decimal price
        float latitude
        float longitude
        char owner_id FK
    }
    REVIEW {
        char id PK
        text text
        int rating
        char user_id FK
        char place_id FK
    }
    AMENITY {
        char id PK
        varchar name UK
    }
    PLACE_AMENITY {
        char place_id PK, FK
        char amenity_id PK, FK
    }