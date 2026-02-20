# 웹프로그래밍 ->파라미터값의 범위를 지정(숫자지정,문자지정?(OK)) => Quey함수 이용
#1.FastAPI 클래스를 가져온다.
from fastapi import FastAPI,Query #데이터의 제한조건을 부여 

#2.FastAPI객체를 생성

app = FastAPI() # 
 
@app.get("/items/")  #URL경로에 변수를 지정(문자,숫자 입력(제약 조건(원하는 데이터만 입력받겠다.)))
#                              1.디폴트값 설정(=기본값) 2.범위해당 옵션 ... 3.title="사용목적"
async def read_items(q: str = Query(None,min_length = 3,max_length = 50,title="검색어"), 
                    limit: int =  Query(10,gt=0,le=100)): # >0  ,<100 (1이상 ~100이하) 
    return {"q": q,"limit": limit } #
#uvicorn datavalidation_3:app --reload


