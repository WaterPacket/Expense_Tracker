import os
jwt_key=os.getenv("JWT_SECRET_KEY")
from connection import manage_connection_resources
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
import psycopg2 as psy
def login_authentication(json_obj):
 with manage_connection_resources() as (conn,cursor):
  try:
    cursor.execute("select password_hash from user_data where user_name=%s", (json_obj.user_name,))
    original_hash_pw = cursor.fetchone()
    if original_hash_pw==None:
        raise HTTPException(status_code=401, detail="Invalid user_name or password ")
    else:
        pw=original_hash_pw[0]
        result=bcrypt.checkpw(json_obj.password.encode(),pw.encode())
        if (result==True):
            cursor.execute("select user_id from user_data where user_name=%s",(json_obj.user_name,))
            user_id=cursor.fetchone()
            user_id=int(user_id[0])
            jwt_token=jwt.encode(
                {"user_id":user_id,
                         "exp":datetime.now(timezone.utc)+timedelta(minutes=30)},
                jwt_key,
                algorithm="HS256"
            )
            return jwt_token
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
  except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
  except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="There is a operational issue in db")
