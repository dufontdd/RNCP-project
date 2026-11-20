```mermaid
erDiagram

    USERS {
        CHAR(36) id PK
        VARCHAR(50) first_name
        VARCHAR(50) last_name
        VARCHAR(120) email
        VARCHAR(128) password
        BOOLEAN is_admin
        DATETIME created_at
        DATETIME updated_at
    }

    MANHWAS {
        CHAR(36) id PK
        VARCHAR(100) title
        TEXT description
        DATETIME created_at
        DATETIME updated_at
    }

    GENRES {
        CHAR(36) id PK
        VARCHAR(50) name
        DATETIME created_at
        DATETIME updated_at
    }

    REVIEWS {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) manhwa_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    MANHWA_GENRE {
        CHAR(36) manhwa_id FK
        CHAR(36) genre_id FK
    }

    USERS ||--o{ REVIEWS : writes
    MANHWAS ||--o{ REVIEWS : receives
    MANHWAS ||--o{ MANHWA_GENRE : has
    GENRES ||--o{ MANHWA_GENRE : classifies
```
