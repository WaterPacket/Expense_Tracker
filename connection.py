import psycopg2 as psy

# this method is used to connect the py with db and creates a conn obj that provides access to the db
def connection():
    conn = psy.connect(
        host="localhost",
        port=5432,
        database="expense_tracker",
        user="postgres",
        password="1"
    )
    # it returns the conn obj if connection succeeds
    # else returns an operational error to the caller
    return conn
