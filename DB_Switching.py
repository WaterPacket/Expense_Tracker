import os
db_table = os.getenv("table_name")
if db_table == "test_expenses":
   table_name = "test_expenses"
else:
    table_name = "expenses"
db_user_data_table_name=os.getenv("user_data_table_name")
if not db_user_data_table_name:
  db_user_data_table_name = "user_data"


