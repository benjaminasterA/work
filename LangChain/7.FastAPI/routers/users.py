#users.py CRUD 관리
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db_connection

#RestAPI 공통 경로 지정
router = APIRouter(prefix = "/users",tags = ["Users"])
# router = APIRouter(prefix = "/ietms",tags = ["ietms"])
# router = APIRouter(prefix = "/payments",tags = ["payments"])

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

#1. Create(insert)
#요청 경로 "/"-> /user/
@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name,email) VALUES (?,?)",
        (user.name,user.email)
    )
    conn.commit()

    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "name": user.name, "email": user.email}

#2. Read(all)
#요청 경로 Get-> /user/
@router.get("/",response_model=List[UserResponse])
def get_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT * FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]

#3. Read(one)
#요청 경로 Get /users/2
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)).fetchone()
    
    conn.close()
    #데이터가 없는 경우 예외 처리한다.
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

#4. Update
#요청 경로 Get /users/2
@router.put("/{user_id}",response_model = UserResponse)
def updated_user(user_id: int, updated_user: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = conn.execute(
        "UPDATE users SET name = ?, email=? WHERE id = ?",
        (updated_user.name,updated_user.email,user_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.close()
    return {"id": user_id, "name": updated_user.name, "email": updated_user.email}

#5. Delete

#요청 경로 Get /users/2
@router.delete("/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.close()
    return {"message": f"user {user_id} deleted successfuly"}
