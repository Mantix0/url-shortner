#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    DO
    \$do\$
    BEGIN
        -- Check for user existence using pg_roles (more standard than pg_user)
        IF NOT EXISTS (
            SELECT FROM pg_roles WHERE rolname = '$POSTGRES_USER'
        ) THEN
            CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
        END IF;

        -- Check for database existence
        IF NOT EXISTS (
            SELECT FROM pg_database WHERE datname = '$POSTGRES_DB'
        ) THEN
            CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;
            GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
        END IF;
    END
    \$do\$;
EOSQL