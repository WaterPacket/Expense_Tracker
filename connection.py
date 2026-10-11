
import psycopg2 as psy

import os

# this method is used to connect the py with db and creates a conn obj that provides access to the db
def connection():
    conn = psy.connect(
        host=os.getenv("DB_HOST_NAME"),
        port=os.getenv("DB_PORT_NUMBER"),
        database=os.getenv("DB_DATABASE_NAME"),
        user=os.getenv("DB_USER_NAME"),
        password=os.getenv("DB_PASSWORD")
    )
    # it returns the conn obj if connection succeeds
    # else returns an operational error to the caller
    return conn


