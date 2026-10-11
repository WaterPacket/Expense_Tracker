import os
from dotenv import load_dotenv
from pathlib import Path
import pytest
import bcrypt

load_dotenv(Path(__file__).parent/"secret_details.env")
load_dotenv(Path(__file__).parent/"test_details.env",override=True)
from connection import connection
con=connection()
@pytest.fixture(scope="session")
def cursor():
    cursor=con.cursor()
    yield cursor
    cursor.close()
    con.close()
@pytest.fixture(autouse=True,scope="session")
def empty_the_tables(cursor):
    cursor.execute("truncate table expenses,user_data restart identity;")
    con.commit()
    password="12345678"
    password=password.encode()
    password=bcrypt.hashpw(password,bcrypt.gensalt())
    password=password.decode()
    cursor.executemany("""insert into user_data (user_name,password_hash)
                       values(%s,%s);""",
                       [("user_one",password),("user_two",password),("user_three",password)])
    con.commit()
    cursor.executemany("""insert into expenses (category,amount,description,date_of_expense,user_id)
                       values(%s,%s,%s,%s,%s)""",
                       [("a",1,"aa","2026-09-01",1),("b",2,"bb","2026-09-02",2),("c",3,"ccc","2026-09-03",3)])
    con.commit()
