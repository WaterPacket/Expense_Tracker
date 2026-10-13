import psycopg2 as psy
from fastapi import HTTPException
from connection import manage_connection_resources

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
