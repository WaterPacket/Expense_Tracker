import os
from dotenv import load_dotenv
from pathlib import Path
import pytest
import bcrypt
from psycopg2.extras import RealDictCursor

load_dotenv(Path(__file__).parent/"secret_details.env")
load_dotenv(Path(__file__).parent/"test_details.env",override=True)
from connection import connection

@pytest.fixture(scope="session")
def cursor(channel):
    cursor=channel.cursor()
    yield cursor
    cursor.close()

@pytest.fixture(scope="session")
def dict_cursor(channel):
    cursor=channel.cursor(cursor_factory=RealDictCursor)
    yield cursor
    cursor.close()

@pytest.fixture(scope="session")
def channel():
    db_name=os.getenv("DB_DATABASE_NAME","")
    if db_name=="test_expense_tracker":
     con=connection()
     yield con
     con.close()
    else:
        raise RuntimeError(f"Database mismatch expected test_expense_tracker found {db_name} !")


@pytest.fixture(autouse=True,scope="session")
def empty_the_tables(cursor,channel):
    cursor.execute("truncate table expenses,user_data restart identity;")
    channel.commit()
    password="12345678"
    password=password.encode()
    password=bcrypt.hashpw(password,bcrypt.gensalt())
    password=password.decode()
    cursor.executemany("""insert into user_data (user_name,password_hash)
                       values(%s,%s);""",
                       [("user_one",password),("user_two",password),("user_three",password),("sk_sabir",password)])
    channel.commit()
    cursor.executemany("""insert into expenses (category,amount,description,date_of_expense,user_id)
                       values(%s,%s,%s,%s,%s)""",
                       [("a",1,"aa","2026-09-01",1),("b",2,"bb","2026-09-02",2),("c",3,"ccc","2026-09-03",3),('d',4,'ddd','2026-09-04',4)])
    channel.commit()
