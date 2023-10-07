from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

users = {
    1:{
        'name':'John',
        'age':20,
        'email':'val@yahoo.com'
    }
}

class User(BaseModel):
    name: str
    age: int
    email: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

#path parameters
@app.get("/get-user/{user_id}")
def get_user(user_id: int = Path( ..., description="User Id of the user you want" , gt=0, lt=3)):
    return users[user_id]


#query parameters
@app.get("/get-user-by-name/")
def get_user_by_name(* ,name: Optional[str] = None, test:int): #asterisk allows us to have default parameters following a non default parameter
    for user_id in users:
        if users[user_id]['name'] == name:
            return users[user_id]
    return {"message": "User not found"}

#combining path and query parameters
@app.get("/get-user-by-parameters/{user_id}")
def get_user_by_parameters(*, user_id ,name: Optional[str] = None, test:int): #asterisk allows us to have default parameters following a non default parameter
    for user_id in users:
        if users[user_id]['name'] == name:
            return users[user_id]
    return {"message": "User not  found"}


@app.post("/create-user/")
def create_user(user_id: int, user: User):
    if user_id in users:
        return {"message": "User already exists"}
    users[user_id] = user
    return {"message": "User created"}


#put method
@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in users:
        return {"message": "User does not exist"}
    
    if user.name != None:
        users[user_id]['name']  = user.name
    if user.age != None:
        users[user_id]['age']  = user.age
    if user.email != None:
        users[user_id]['email']  = user.email

    return users[user_id]

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        return {"message": "User does not exist"}
    del users[user_id]
    return {"message": "User deleted"}