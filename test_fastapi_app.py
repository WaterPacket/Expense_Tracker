import os
import jwt
from fastapi.testclient import TestClient
from fastapi_app import app
client=TestClient(app)



# ===================================== TESTING THE REGISTRATION BEHAVIOUR ==========================================

def test_without_username():
    response=client.post("/user-registration",
                         json={"password":"12345678"})
    assert response.status_code==422

def test_without_password():
    response=client.post("/user-registration",
                         json={"user_name":"12345678"})

    assert response.status_code==422

def test_short_invalid_username():
    response=client.post("/user-registration",
                         json={"user_name":"1234567",
                               "password":"12345678"})
    assert response.status_code==422

def test_long_invalid_username():
    response=client.post("/user-registration",
                         json={"user_name":"1234567890123456789012345",
                               "password":"12345678"})
    assert response.status_code==422

def test_valid_username_short_invalid_password():
    response=client.post("/user-registration",
                         json={"user_name":"12345678",
                               "password":"1234567"})
    assert response.status_code==422

def test_valid_username_long_invalid_password():
    response=client.post("/user-registration",
                         json={"user_name":"123456789",
                               "password":"1234567890123456789012345"})
    assert response.status_code==422

#here by testing this case i found out a behaviour
#when i ran this case with same successful registered users details the program showing error 409
#i forgot to check how the application behave if i try to register with existing user_name

# def test_valid_username_valid_password():#while executing change the details to test otherwise u will get a error
#     response=client.post("/user-registration",json={"user_name":"nandamuri_fuk","password":"12345678"})
#     assert response.status_code==200

def test_valid_username_valid_password():
    response=client.post("/user-registration",
                         json={"user_name": "sk_sabir",
                               "password": "12345678"}
                         )
    print(response.text)
    assert response.status_code==200
    assert response.json()=="User Registration Successful"


def test_registration_with_existing_username():
    response=client.post("/user-registration",
                         json={"user_name":"sk_sabir",
                               "password":"12345678"})
    assert response.status_code==409



# ================================== TESTING THE LOGIN BEHAVIOUR ==================================================

def test_login_without_username():
    response=client.post("/user-login",
                         json={"password":"12345678"})
    assert response.status_code==422

def test_login_without_password():
    response=client.post("/user-login",
                         json={"user_name":"12345678"})
    assert response.status_code==422


def test_login_short_invalid_username():
    response=client.post("/user-login",
                         json={"user_name":"1234567",
                               "password":"12345678"})
    assert response.status_code==422

def test_login_long_invalid_username():
    response=client.post("/user-login",
                         json={"user_name":"1234567890123456789012345",
                               "password":"12345678"})
    assert response.status_code==422

def test_login_valid_username_long_invalid_password():
    response=client.post("/user-login",
                         json={"user_name":"123456789012345678901234",
                                "password":"1234567890123456789012345"})
    assert response.status_code==422

def test_login_valid_username_short_invalid_password():
    response=client.post("/user-login",
                         json={"user_name":"123456789012345678901234",
                                "password":"1234567"})
    assert response.status_code==422

def test_login_valid_username_not_registered():
    response=client.post("/user-login",
                         json={"user_name":"12345678",
                               "password":"12345678"})
    assert response.status_code==401

def test_login_valid_username_invalid_password():
    response=client.post("/user-login",
                         json={"user_name":"sk_sabir",
                               "password":"123456789"})
    assert response.status_code==401

def test_login_valid_username_valid_password():
    response=client.post("/user-login",
                         json={"user_name":"sk_sabir",
                               "password":"12345678"})
    assert response.status_code==200
    token=response.json()
    assert isinstance(token,str)

# ========================== TESTING THE ADD-EXPENSE END-POINT ============================================

# ------------------------------------------- CHECKING THE BEHAVIOUR FOR TOKENS -----------------------------------

def test_behaviour_without_token():
 response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 1000,
                               "description": "qwe",
                               "date_of_expense": "2023-09-01"}
                      )
 assert response.status_code==401
def test_behaviour_with_invalid_token():
 jwt_token = client.post("/user-login",
                         json={"user_name": "sk_sabir",
                               "password": "12345678"})
 jwt_token = jwt_token.json()
 header = {"Authorization": f"Bearer {jwt_token}1"}

 response = client.post("/add-expense",
                        json={"category": "10",
                              "amount": 1000,
                              "description": "qwe",
                              "date_of_expense": "2026-09-01"},
                        headers=header)
 assert response.status_code == 401


#-------------------------------------- TESTING BEHAVIOUR WITH VALID TOKEN AND INVALID PROPERTIES --------------------------

def test_properties_valid_token_missing_properties():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 1000,
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_invalid_category():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": 10,
                               "amount": 1000,
                               "description": "qwe",
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_zero_amount():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 0,
                               "description": "qwe",
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_negative_amount():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": -1000,
                               "description": "qwe",
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_invalid_amount():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": "thousand",
                               "description": "qwe",
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_invalid_description():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 1000,
                               "description": 10,
                               "date_of_expense": "2026-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_invalid_date():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 1000,
                               "description": "qwe",
                               "date_of_expense": 2026},
                         headers=header)
    assert response.status_code==422

def test_properties_invalid_dateformat():
    jwt_token=client.post("/user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    jwt_token=jwt_token.json()
    header={"Authorization":f"Bearer {jwt_token}"}

    response=client.post("/add-expense",
                         json={"category": "10",
                               "amount": 1000,
                               "description": "qwe",
                               "date_of_expense": "20-09-01"},
                         headers=header)
    assert response.status_code==422

def test_properties_all_valid():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}

    response = client.post("/add-expense",
                           json={"category": "10",
                                 "amount": 1000,
                                 "description": "qwe",
                                 "date_of_expense": "2026-09-01"},
                           headers=header)
    assert response.status_code == 200
    assert response.json()=="Expense added successfully"



# ==================================== TESTING THE VIEW-EXPENSE END-POINT =================================

# for this endpoint there are no parameters
# we will just need to test the token behaviour

def test_view_exp_without_token():
    response=client.get("/view-expense")
    assert response.status_code==401

def test_view_exp_with_invalid_token():
    uid_token=client.post("user-login",
                          json={"user_name":"sk_sabir",
                                "password":"12345678"})
    uid_token=uid_token.json()
    header_data={"Authorization":f"Bearer {uid_token}1"}
    response=client.get("/view-expense",
                         headers=header_data)
    assert response.status_code==401

def test_view_exp_with_valid_token(cursor):
    uid_token=client.post("user-login",
                          json={"user_name":"user_one",
                                "password":"12345678"})
    uid_token=uid_token.json()
    header_data={"Authorization":f"Bearer {uid_token}"}
    res=client.get("/view-expense",
                         headers=header_data)
    response=res.json()

    assert res.status_code==200 # checking if the operation succeded or not

    assert isinstance(response,list) # checking the output is a list or not

    for r in response:
        assert isinstance(r, dict)  # checking the elements in the list dicts or not
        keys = list(r.keys())  # fields  of the response dict
        key = 0
        column_names = ["sno", "category", "amount", "description", "date_of_expense"]  # fields of dict
        for col_name in column_names:  # checking the structure and looking does the key exists or not in a sequence
            assert col_name == keys[key]
            key = key + 1

    uid_tkn=uid_token
    uid_dict=jwt.decode(uid_tkn,os.getenv("JWT_SECRET_KEY"),algorithms=["HS256"])
    uid=uid_dict["user_id"]
    cursor.execute("select sno,category,amount,description,date_of_expense from expenses where user_id=%s order by sno asc",
                   (uid,))
    user_expenses=cursor.fetchall()
    dict_values = []
    list_values = user_expenses
    for tuple_value in list_values:
        field_value = 0
        dict_value = {
            "sno": None,
            "category": None,
            "amount": None,
            "description": None,
            "date_of_expense": None}

        for key in dict_value:
            if(key=="amount" or key=="date_of_expense"):
                dict_value[key] = str(tuple_value[field_value])
                field_value =field_value+ 1
            else:
                dict_value[key] = (tuple_value[field_value])
                field_value =field_value+ 1

        dict_values.append(dict_value)

    assert response==dict_values

# ============================== TESTING THE BEHAVIOUR OF THE UPDATE ENDPOINT =================================================

#------------------------------------- TESTING BEHAVIOUR WITH TOKENS ----------------------------------------

def test_update_exp_without_token():
    response = client.put("/update-expense",
                           json={"sno": 10,
                                 "amount": 1000}
                           )
    assert response.status_code == 401

def test_update_exp_with_invalid_token():
 jwt_token = client.post("/user-login",
                         json={"user_name": "user1",
                               "password": "12345678"})
 jwt_token = jwt_token.json()
 header = {"Authorization": f"Bearer {jwt_token}1"}
 response = client.put("/update-expense",
                           json={"sno": 10,
                                 "amount": 1000},
                           headers=header
                           )
 assert response.status_code == 401

# ------------------------------------- TESTING BEHAVIOUR WITH VALID TOKEN -------------------------

def test_update_exp_valid_tkn_no_sno():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={ "amount": 1000},
                        headers=header
                        )
    assert response.status_code==422

def test_update_exp_valid_tkn_no_amount():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={ "sno": 50},
                        headers=header
                        )
    assert response.status_code==422

def test_update_exp_valid_tkn_invalid_sno_dt():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={"sno": "tenssw",
                              "amount": 1000},
                        headers=header
                        )
    assert response.status_code==422

def test_update_exp_valid_tkn_invalid_amount_dt():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={"sno": "10",
                              "amount": "thousand"},
                        headers=header
                        )
    assert response.status_code==422

def test_update_exp_valid_tkn_invalid_sno():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={"sno": 100,
                              "amount": 1000},
                        headers=header
                        )
    assert response.status_code==404

def test_update_exp_valid_tkn_invalid_amount():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={"sno": 10,
                              "amount": 0},
                        headers=header
                        )
    assert response.status_code==422

def test_update_exp_valid_tkn_valid_amount_invalid_sno():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    header=jwt_token.json()
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json={"sno": 10000,
                              "amount": 10},
                        headers=header
                        )
    assert response.status_code==404

def test_update_exp_valid_tkn_valid_amount_valid_sno(cursor):
    jwt_token = client.post("/user-login",
                            json={"user_name": "user_one",
                                  "password": "12345678"})
    header=jwt_token.json()
    user_input={"sno":1,"amount":1000}
    header={"Authorization":f"Bearer {header}"}
    response=client.put("/update-expense",
                        json=user_input,
                        headers=header
                        )
    assert response.status_code==200
    assert response.json()=="Updated the value successfully"

    jwt_uid=jwt.decode(jwt_token.json(),os.getenv("JWT_SECRET_KEY"),algorithms=["HS256"])
    uid=jwt_uid["user_id"]
    cursor.execute("select amount from expenses where user_id=%s and sno=%s",(uid,user_input["sno"]))
    db_amount=cursor.fetchone()
    db_amount=(db_amount[0])
    assert db_amount==user_input["amount"]




# ================================== TESTING THE SEARCH EXPENSE ENDPOINT =========================================

# ----------------------------------- TESTING BEHAVIOUR WITH INVALID TOKEN ---------------------------------------------

def test_search_exp_without_token():
    response=client.request("get","/search-expense",
                            params={"date_of_expense":"2026-09-23"})
    assert response.status_code==401

def test_search_exp_with_invalid_token():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}1"}
    response = client.request("get","/search-expense",
                           params={"date_of_expense": "2026-09-23"}
                           ,headers=header)
    assert response.status_code==401

# ---------------------------------- TESTING THE BEHAVIOUR WITH VALID TOKEN --------------------------------------------

def test_search_exp_with_valid_token_without_date():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/search-expense"
                           , headers=header)

    assert response.status_code == 422

def test_search_exp_with_valid_token_invalid_date_dt():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("get","/search-expense",
                           params={"date_of_expense": 10}
                           , headers=header)

    assert response.status_code == 422

def test_search_exp_with_valid_token_invalid_date():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("get","/search-expense",
                           params={"date_of_expense": "2000-00-00"}
                           , headers=header)

    assert response.status_code == 422

def test_search_exp_with_valid_token_valid_date_not_found():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/search-expense",
                           params={"date_of_expense": "2000-01-01"}
                           , headers=header)
    assert response.status_code == 200
    assert response.json()==[]

def test_search_exp_with_valid_token_valid_date(cursor):
    jwt_token = client.post("/user-login",
                            json={"user_name": "user_two",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    user_input={"date_of_expense":"2026-09-02"}
    response = client.get("/search-expense",
                              params=user_input
                              ,headers=header)

    assert response.status_code == 200
    uid=jwt.decode(jwt_token,os.getenv("JWT_SECRET_KEY"),algorithms=["HS256"])
    uid=uid["user_id"]
    date_of_expense=user_input["date_of_expense"]
    cursor.execute("select sno,category,amount,description,date_of_expense from expenses where user_id=%s and date_of_expense=%s order by sno asc ",(uid,date_of_expense))
    db_data=cursor.fetchall()
    output=[]
    list_=db_data
    for tuple_value in list_:
        dict_value = {"sno": None,
                      "category": None,
                      "amount": None,
                      "description": None,
                      "date_of_expense": None}
        tuple_ind=0
        for key in dict_value:
            if key=="amount" or key=="date_of_expense":
                dict_value[key]=str(tuple_value[tuple_ind])
                tuple_ind=tuple_ind+1
            else:
                dict_value[key] = tuple_value[tuple_ind]
                tuple_ind = tuple_ind + 1
        output.append(dict_value)

    assert output==response.json()


# ========================== TESTING BEHAVIOUR FOR DELETE EXPENSE ENDPOINT =============================================

# for test-client doesnt support the json for delete method
# so we are using request method where we can pass the request to endpoint

def test_delete_exp_without_token():
    response = client.request("delete","/delete-expense",
                                 json={"sno": 10}
                             )
    assert response.status_code == 401

def test_delete_exp_with_invalid_token():
 jwt_token = client.post("/user-login",
                         json={"user_name": "sk_sabir",
                               "password": "12345678"})
 jwt_token = jwt_token.json()
 header = {"Authorization": f"Bearer {jwt_token}1"}
 response = client.request("delete","/delete-expense",
                           params={"sno":10},
                           headers=header
                           )
 assert response.status_code == 401

# ----------------------------- TESTING THE BEHAVIOUR WITH VALID TOKEN -------------------------------------

def test_delete_exp_with_valid_token_no_sno():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("delete", "/delete-expense",
                              headers=header
                              )
    assert response.status_code == 422

def test_delete_exp_with_valid_token_invalid_sno_dt():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("delete", "/delete-expense",
                              params={"sno": "ten"},
                              headers=header
                              )
    assert response.status_code == 422

def test_delete_exp_with_valid_token_invalid_sno():
    jwt_token = client.post("/user-login",
                            json={"user_name": "sk_sabir",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("delete", "/delete-expense",
                              params={"sno": 10000},
                              headers=header
                              )
    assert response.status_code == 404

def test_delete_exp_with_valid_token_valid_sno(cursor):
    jwt_token = client.post("/user-login",
                            json={"user_name": "user_three",
                                  "password": "12345678"})
    jwt_token = jwt_token.json()
    user_input = {"sno": 3}
    header = {"Authorization": f"Bearer {jwt_token}"}
    response = client.request("delete", "/delete-expense",
                              params=user_input,
                              headers=header
                              )
    assert response.status_code == 200
    assert response.json()=="The expense is deleted successfully"
    uid_token=jwt_token
    uid=jwt.decode(uid_token,os.getenv("JWT_SECRET_KEY"),algorithms=["HS256"])
    uid=uid["user_id"]
    cursor.execute("select * from expenses where user_id=%s and sno=%s",(uid,user_input["sno"]))
    db_data=cursor.fetchone()
    assert db_data==None






