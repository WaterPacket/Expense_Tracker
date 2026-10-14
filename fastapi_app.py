import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent/"secret_details.env")
from datetime import date
import jwt
from decimal import Decimal
from Operations import add_expense
from Operations import view_expenses
from Operations import update_expense
from Operations import delete_expense
from Operations import search_expense
from Operations import user_registration
from Operations import login_authentication
from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.security import HTTPBearer
from fastapi import Depends
from fastapi import HTTPException


jwt_key=os.getenv("JWT_SECRET_KEY")

class Login_Validation(BaseModel):
    user_name:str=Field(min_length=8,max_length=24)
    password:str=Field(min_length=8,max_length=24)

class User_Registration(BaseModel):
    user_name:str=Field(min_length=8,max_length=24)
    password:str=Field(min_length=8,max_length=24)

class Add_Expense(BaseModel):
    category:str
    #checking the value even its integer it must be >0.
    amount:Decimal=Field(gt=0)
    description:str
    date_of_expense:date

class Update_Expense(BaseModel):
    sno:int=Field(gt=0)
    amount:Decimal=Field(gt=0)

class Delete_Expense(BaseModel):
    sno:int=Field(gt=0)

class Search_expense(BaseModel):
    date_of_expense:date
#Response_Models
class res_get_expense(BaseModel):
    sno:int
    category:str
    amount:Decimal=Field(gt=0)
    description:str
    date_of_expense:date

app=FastAPI()

security=HTTPBearer()

def extract_uid(cred = Depends(security)):
 try:
    token=cred.credentials
    uid=jwt.decode(token,jwt_key,algorithms=["HS256"])
    return uid["user_id"]
 except jwt.InvalidTokenError:
     raise HTTPException(status_code=401,detail="Invalid token")

@app.get("/view-expense",response_model=list[res_get_expense])
def get__expense(uid=Depends(extract_uid)):
    return view_expenses(uid)

@app.post("/add-expense")
def add__expense(json_obj:Add_Expense,uid=Depends(extract_uid)):
    return add_expense(json_obj,uid)

@app.put("/update-expense")
def update__expense(data:Update_Expense,uid=Depends(extract_uid)):
    return update_expense(data,uid)

@app.delete("/delete-expense")
def delete__expense(sno:int,uid=Depends(extract_uid)):
    return delete_expense(sno,uid)

@app.get("/search-expense",response_model=list[res_get_expense])
def search__expense(date_of_expense:date,uid=Depends(extract_uid)):
    return search_expense(uid,date_of_expense)

@app.post("/user-registration")
def user__registration(json_obj:User_Registration):
 return user_registration(json_obj)

@app.post("/user-login")
def user__login(json_obj:Login_Validation):
    return login_authentication(json_obj)
