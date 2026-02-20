# 웹프로그래밍 ->파라미터값을 어떻게 전달->어떻게 전달받는지에 대한 개념
#1.FastAPI 클래스를 가져온다.
from fastapi import FastAPI 

#2.FastAPI객체를 생성

app = FastAPI() # 
 
#3.접속=>상품구매(items)->검색인데 대분류에 해당
#   /items/3 =>상품의 item_id가 3번인 데이터를 보여주세요   =>{전달할 변수명}  /items/"3"     
@app.get("/items/{item_id}")  #URL경로에 변수를 지정
def read_item(item_id: int): # 변수명:자료형 =>타입힌트로 int 지정->자동 검증
    return {"item_id": item_id } #요청경로의 숫자를 그대로 반환

#   /items?skip=5&limit=10  ~?매개변수명=전달할값&매개변수명2=전달할값2&... =>페이지 데이터 공유X
#                          검색인데 중,소분류
# 비동기 처리 해주는 함수의 의미
@app.get("/items") #함수에서 매개변수를 전달X =>디폴트값(=기본값) 
async def read_item(skip: int = 0,limit: int = 10 ): 
    #skip,limit은 URL경로에 없지만 ?skip=0&limt=10 형태로 전달 받을 수 있다.
    return {"skip": skip,"limit" : limit }
# uvicorn pathparameter_2:app --reload

