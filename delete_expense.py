import psycopg2 as psy
from connection import connection
from fastapi import HTTPException

def delete_expense(sno,uid):
 try:
   conn=connection()
   cursor=conn.cursor()
   try:
      # sending the query to delete the expense

     cursor.execute("delete from expenses where user_id=%s and sno=%s", (uid,sno))

      # counts how many no of rows effected if the query is executed

     if (cursor.rowcount > 0):
         # we only commit if it changes any row
         # if no row effected the sno of the row is invalid
         conn.commit()
         return "The expense is deleted successfully"
     else:
         raise HTTPException(status_code=404,detail="Given sno is invalid !")

   except psy.OperationalError:
       raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
   except psy.DatabaseError:
      # returns msg if there is a problem in the query
      raise HTTPException(status_code=500,detail="problem in internal db")
   finally:
     # closing resources after usage
     cursor.close()
     conn.close()

 except psy.OperationalError:
       # tell the user the connction was not established
       raise HTTPException(status_code=503, detail="db connection problem")
