import psycopg2 as psy
from contextlib import contextmanager
from fastapi import HTTPException
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

@contextmanager
def manage_connection_resources(cursor_type=None):
 cursor=None
 try:
  channel=connection()
  try:
    cursor = channel.cursor(cursor_factory=cursor_type)
    yield channel, cursor
  finally:
      if not cursor==None:
        cursor.close()
        channel.close()
      else:
          channel.close()
 except psy.OperationalError:
   raise HTTPException(status_code=503,detail="DB connection failure")