import psycopg2 as psy
from connection import manage_connection_resources
from fastapi import HTTPException
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
