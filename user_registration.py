import psycopg2 as psy
import bcrypt
from connection import manage_connection_resources
from fastapi import HTTPException

def user_registration(json_obj):

  with manage_connection_resources() as (conn,cursor):
    try:
      password=json_obj.password
      password=password.encode()
      password=bcrypt.hashpw(password,bcrypt.gensalt())
      password=password.decode()
      cursor.execute("insert into user_data (user_name,password_hash) values (%s,%s)",(json_obj.user_name,password))
      conn.commit()
      return "User Registration Successful"
    except psy.errors.UniqueViolation :
         raise HTTPException(status_code=409 , detail="username already exists")
    except psy.OperationalError:
         raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
    except psy.DatabaseError:
         raise HTTPException(status_code=500, detail="problem in the internal db")