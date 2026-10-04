import psycopg2 as psy

# used for password hashing and validation
import bcrypt

from connection import connection

from fastapi import HTTPException

from DB_Switching import table_name as db_table_name , db_user_data_table_name as user_table


def user_registration(json_obj):

 try:
     con=connection()
     cursor=con.cursor()
     cursor.execute(f"select user_name from {user_table} where user_name=%s",(json_obj.user_name,))
     user_name=cursor.fetchone()
     if(user_name==None):
         user_name=json_obj.user_name
         password=json_obj.password
     else:
         raise HTTPException(status_code=409,detail="username already exists")

     password = password.encode()
     password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
     password_hash = password_hash.decode()
     try:
      cursor.execute(f"insert into {user_table} (user_name,password_hash)values(%s,%s)",
                   (user_name,password_hash))
      con.commit()
      return "User Registration Successful"
     except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="There is a problem in db operation")
     finally:
      cursor.close()
      con.close()
 except psy.OperationalError:
     raise HTTPException(status_code=503,detail="There is a problem in db connection")