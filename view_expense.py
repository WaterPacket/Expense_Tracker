import psycopg2 as psy
from psycopg2.extras import RealDictCursor

from connection import manage_connection_resources
from fastapi import HTTPException
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
