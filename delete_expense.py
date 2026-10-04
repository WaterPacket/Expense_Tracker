import psycopg2 as psy
from connection import connection
from fastapi import HTTPException
from DB_Switching import table_name as db_table_name

# this method delete the expense recored based on its number given by user

table_name=db_table_name

def delete_expense(data,uid):
 try:

  # building conn obj and building cursor obj to send query through the conn to db

  conn=connection()
  cursor=conn.cursor()
  try:
      # sending the query to delete the expense

     cursor.execute(f"delete from {table_name} where user_id=%s and sno=%s", (uid,data.sno))

      # counts how many no of rows effected if the query is executed

     if (cursor.rowcount > 0):

         # we only commit if it changes any row
         # if no row effected the sno of the row is invalid

         conn.commit()

         return ("The expense is deleted successfully")
     else:
         raise HTTPException(status_code=404,detail="Given sno is invalid !")
  except psy.DatabaseError:

      # returns msg if there is a problem in the query

      raise HTTPException(status_code=503,detail="There is an internal problem in the db")
  finally:

     # closing resources after usage

     cursor.close()
     conn.close()
 except psy.OperationalError:

     # tell the user the connction was not established

     raise HTTPException(status_code=500,detail="There is a problem in DB connection")