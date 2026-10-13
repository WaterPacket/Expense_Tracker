import psycopg2 as psy
from connection import manage_connection_resources
from fastapi import HTTPException
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
