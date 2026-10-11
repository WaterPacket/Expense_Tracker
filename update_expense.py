import psycopg2 as psy
from fastapi import HTTPException
from connection import connection

def update_expense(data,uid):
 try:
  # building conn obj and building cursor obj to send query through the conn to db
  conn_obj=connection()
  cursor=conn_obj.cursor()
  try:
    # sending the query to update the amount
    cursor.execute("update expenses set amount=%s where user_id=%s and sno=%s",
                   (data.amount,uid,data.sno))
    # counts how many no of rows effected if the query is executed
    rows_effected=cursor.rowcount
    if rows_effected>0:
     # we only commit if it changes any row
     # if no row effected the sno of the row is invalid
     conn_obj.commit()
     return("Updated the value successfully")
    else:
        raise HTTPException(status_code=404,detail="sno not found !")
  except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
  except psy.DatabaseError:
      raise HTTPException(status_code=500,detail="Internal DB problem try again later")
  finally:
     # closing resources after usage
     cursor.close()
     conn_obj.close()
 except psy.OperationalError:
     # tell the user the connction was not established
  raise HTTPException(status_code=503,detail="There is a issue in DB try after sometime")