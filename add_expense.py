import psycopg2 as psy

from connection import connection

from fastapi import HTTPException

from DB_Switching import table_name as db_table_name

table_name=db_table_name

def add_expense(expense,id):
 try:

  # try to build the connection obj
  # build the cursor obj by which we pass querys to db through conn obj

  conn=connection()
  cursor = conn.cursor()

  try:

      # getting the expense data from the frontend Validated by the pydentic base model
      cursor.execute(
      f"insert into {table_name} (user_id,category,amount,description,date_of_expense)values(%s,%s,%s,%s,%s)",
      (id,expense.category,expense.amount,expense.description,expense.date_of_expense)
      )
      # we had to commit the connection.obj when our query make changes in the db .
      conn.commit()
      return ("Expense added successfully")

  except psy.DatabaseError:

   raise HTTPException(status_code=500, detail="Internal DB problem try again later")

  # closing the resources after the operation is completed

  finally:
      cursor.close()
      conn.close()

 # if failed to build the connection obj we stop this operation
 # if its value validation we give chance to re enter but its a db connection issue user cant do anything

 except psy.OperationalError:
     raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")