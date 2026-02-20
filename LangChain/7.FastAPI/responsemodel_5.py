# 값을 입력을 받아서 검증=>class를 통해서 검증이 가능하다.
#1.FastAPI 클래스를 가져온다.
from fastapi import FastAPI 
from pydantic import BaseModel #데이터 검증 및 스키마 정의용(=DB)
#추가
from typing import Optional

class User(BaseModel): 
    username: str
    #email: str =>반드시 이메일 필수인 경우
    email:Optional[str] = None # 형식) Optional[입력받는 자료형] = None
                # email는 반드시 입력해야 하는 필드가 아니라 선택적으로 입력을 허용해주는 경우 
                # "문자열" 또는 None을 허용한다는 의미 (기본값으로 None으로 설정했다는  표시    
   
#2.FastAPI객체를 생성
app = FastAPI() # 
 # /users/23  함수뒤에 ,response_model=User(사용자정의 자료형)=>전달받은 객체는 User를 의미
 #  select  username   from User
@app.get("/users/{username}",response_model=User)  # 
def get_user(username : str): # (item_name:str, item_price:float,is_offer:bool,,,,,,,,)
    return User(username=username) #username(멤버변수)=전달받은 매개변수(익명객체)
#uvicorn postmodel_4:app --reload
# 익명객체 => 이름이 없는 객체(무명씨,작자미상)
#  객체명 = 클래스명()    객체명.멤버변수=값
#  us = User(username=username)
#  return us  
#  >uvicorn responsemodel_5:app --reload