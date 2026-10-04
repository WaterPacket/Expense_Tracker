from connection import connection

from fastapi import HTTPException

import jwt

import bcrypt

import psycopg2 as psy

from DB_Switching import db_user_data_table_name as user_table , table_name as expense_table

def login_authentication(json_obj):
 try:
  conn = connection()
  cursor = conn.cursor()
  try:
    cursor.execute(f"select password_hash from {user_table} where user_name=%s", (json_obj.user_name,))
    original_hash_pw = cursor.fetchone()
    if original_hash_pw==None:
        raise HTTPException(status_code=401, detail="Invalid user_name or password ")
    else:
        pw=original_hash_pw[0]
        result=bcrypt.checkpw(json_obj.password.encode(),pw.encode())
        if (result==True):
            cursor.execute(f"select user_id from {user_table} where user_name=%s",(json_obj.user_name,))
            user_id=cursor.fetchone()
            user_id=int(user_id[0])
            jwt_token=jwt.encode(
                {"user_id":user_id},
                "secret_key",
                 "HS256"
            )
            return jwt_token


        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

  except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="There is a operational issue in db")
  finally:
      cursor.close()
      conn.close()
 except psy.OperationalError:
     raise HTTPException(status_code=503,detail="There is a connection issue in db")