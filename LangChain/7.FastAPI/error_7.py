
from fastapi import FastAPI,HTTPException #불러오는 모듈이 같으면 ,로 구분해서 불러올것
#from fastapi import HTTPEXCEPTION
app = FastAPI() 
 
#3.접속->Get방식(=SQL select에 해당)
@app.get("/error/") 
def raise_error(): 
    #404에러 발생->요청한 데이터가 없을때 발생 404 ,500 문법에러
    raise HTTPException(status_code=404,detail="Item not found")
#1.서버의 상태코드값, datail="이유"
# uvicorn error_7:app --reload   => /  404
