import psycopg2 as psy

from connection import connection

from fastapi import HTTPException

def view_expenses(uid):
 # we are buiulding connection obj to send querys to db

 try:
  channel=connection()
  cursor=channel.cursor()

  try:
    # after conn established we are sending query to  db to retrieve the data
    cursor.execute("Select sno,category,amount,description,date_of_expense from expenses where user_id=%s order by sno asc",(uid,))
    #the cursor holds the retrieves data so we use fetch method to extract data from it
    expenses=cursor.fetchall()
  except psy.OperationalError:
      raise HTTPException(status_code=503, detail="There is a issue in DB try after sometime")
  except psy.DatabaseError:
      # there will be a chance of change of property or problem in query
      # that time we will tell the user there is a db problem
      raise HTTPException(status_code=500, detail="Internal DB problem try again later")

  finally:
    # closing the resources after the usage
     cursor.close()
     channel.close()

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