import psycopg2 as psy

from connection import connection

from fastapi import HTTPException

from DB_Switching import table_name as db_table_name

table_name=db_table_name

def search_expense(uid,date_of_exp):
#query parameter the parameter for the method will be sent directly to the method
# from http request
  try:
    conn=connection()
    cursor=conn.cursor()
    try:
     cursor.execute(f"select * from {table_name} where user_id=%s and date_of_expense=%s",(uid,date_of_exp))
     outcome=cursor.fetchall()
     list_=outcome
     if not list_:
         raise HTTPException(status_code=404,detail="There is no expense on this date ")
     output=[]
     for tuple_value in list_:
         tuple_ind=0
         dict_ = {"sno": None,
                     "category": None,
                     "amount": None,
                     "description": None,
                     "date_of_expense": None,
                     }
         for dict_val in dict_:
             dict_[dict_val]=tuple_value[tuple_ind]
             tuple_ind+=1
         output.append(dict_)
     return output
    except psy.DatabaseError as error :
     print(error)
     raise HTTPException(status_code=500,detail="There is a internal problem in db ")
    finally:
        cursor.close()
        conn.close()
  except psy.OperationalError:
      raise HTTPException(status_code=503,detail="There is a connection problem with db")