import psycopg2 as psy

from connection import connection

from fastapi import HTTPException

from DB_Switching import table_name as db_table_name

table_name=db_table_name

def view_expenses(uid):
 # we are buiulding connection obj to send querys to db

 try:
  channel=connection()
  cursor=channel.cursor()

  try:
    # after conn established we are sending query to  db to retrieve the data
    cursor.execute(f"Select * from {table_name} where user_id=%s order by sno asc",(uid,))
    #the cursor holds the retrieves data so we use fetch method to extract data from it
    expenses=cursor.fetchall()

  except psy.DatabaseError:
      # there will be a chance of change of property or problem in query
      # that time we will tell the user there is a db problem
      raise HTTPException(status_code=500, detail="Internal DB problem try again later")

  finally:
    # closing the resources after the usage
     cursor.close()
     channel.close()
  # this method returns the data of stored expenses as a list[]
  # we want the recorded expenses as dict instead of tuple
  # because dict can only be cnverted to json
  dict_values = []
  list_values = expenses

  for tuple_value in list_values:
      field_value = 0
      dict_value = {
          "sno": None,
          "category": None,
          "amount": None,
          "description": None,
          "date_of_expense": None}

      for key in dict_value:
          dict_value[key] = tuple_value[field_value]
          field_value += 1
      dict_values.append(dict_value)
  return dict_values
 # if connection obj was not created then we will tell the user there is problem in db connection

 except psy.OperationalError:
     
     raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")