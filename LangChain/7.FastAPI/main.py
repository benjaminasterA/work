
from fastapi import FastAPI 
#users테이블과 연결
from routers import users #라우터 import
#from routers import items
app = FastAPI() 
 
#3.접속->Get방식(=SQL select에 해당)
@app.get("/")  #HTTP GET 요청명령어 "/" 로 요청 =>함수로 만들어서 호출 
def read_root(): #FAST API =>접속=>결과물을 반환(json형태(key,value))
    return {"message": "FastAPI Server Running" } #서버 동작 확인용 

#라우터 연결
app.include_router(users.router) #users 라우터 등록
#app.include_router(items.router)
#uvicorn main:app --reload
