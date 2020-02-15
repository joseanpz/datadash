CREATE TABLE public.users (
    id                SERIAL PRIMARY KEY,    
    email             VARCHAR(100) UNIQUE,
    hashed_password   VARCHAR(100),       
    is_active         BOOLEAN,
    is_superuser      BOOLEAN,
    full_name         VARCHAR(100)
);
