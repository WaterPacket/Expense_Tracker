import os
jwt_key=os.getenv("JWT_SECRET_KEY")
import psycopg2 as psy
import bcrypt
from connection import manage_connection_resources
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import jwt
from psycopg2.extras import RealDictCursor

#=========================================== USER REGISTRATION =========================================

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

# ======================================== USER LOGIN ========================================================

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

# ====================================== ADD EXPENSE ===========================================================

def add_expense(expense,id):
 with manage_connection_resources() as (conn,cursor):
  try:
      cursor.execute(
      "insert into expenses (user_id,category,amount,description,date_of_expense)values(%s,%s,%s,%s,%s)",
      (id,expense.category,expense.amount,expense.description,expense.date_of_expense) )
      conn.commit()
      return ("Expense added successfully")
  except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
  except psy.DatabaseError:
   raise HTTPException(status_code=500, detail="Internal DB problem try again later")

#======================================= VIEW EXPENSE ========================================================

def view_expenses(uid):
 with manage_connection_resources(RealDictCursor) as (conn,cursor) :
  try:
    cursor.execute("Select sno,category,amount,description,date_of_expense from expenses where user_id=%s order by sno asc",(uid,))
    expenses=cursor.fetchall()
    return expenses
  except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
  except psy.DatabaseError:
      raise HTTPException(status_code=500, detail="Internal DB problem try again later")


#============================================ UPDATE EXPENSE ===============================================

def update_expense(data,uid):

  with manage_connection_resources() as (conn,cursor):
   try:
    cursor.execute("update expenses set amount=%s where user_id=%s and sno=%s",
                   (data.amount,uid,data.sno))
    rows_effected=cursor.rowcount
    if rows_effected>0:
     conn.commit()
     return("Updated the value successfully")
    else:
        raise HTTPException(status_code=404,detail="sno not found !")
   except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
   except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="Internal DB problem try again later")

#============================================ SEARCH EXPENSE ======================================================

def search_expense(uid,date_of_exp):
 with manage_connection_resources(RealDictCursor) as (conn,cursor):
    try:
     cursor.execute("select sno,category,amount,description,date_of_expense from expenses where user_id=%s and date_of_expense=%s order by sno asc",(uid,date_of_exp))
     outcome=cursor.fetchall()
     return outcome
    except psy.OperationalError:
        raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
    except psy.DatabaseError :
     raise HTTPException(status_code=500,detail="There is a internal problem in db ")


#=============================================== DELETE EXPENSE ===============================================

def delete_expense(sno,uid):
    with manage_connection_resources() as (conn,cursor):
     try:
       cursor.execute("delete from expenses where user_id=%s and sno=%s", (uid,sno))
       if (cursor.rowcount > 0):
         conn.commit()
         return "The expense is deleted successfully"
       else:
         raise HTTPException(status_code=404,detail="Given sno is invalid !")
     except psy.OperationalError:
       raise HTTPException(status_code=503, detail="db connection problem")
     except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="problem in internal db")


