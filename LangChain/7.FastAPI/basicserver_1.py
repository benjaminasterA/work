#basicserver(1).py

#1.FastAPI 클래스를 가져온다.
from fastapi import FastAPI #Fast API를 사용하게 해주는 클래스

#2.FastAPI객체를 생성->1.데이터 저장목적 2.특정한 메서드 호출이 필요=>이것 때문

app = FastAPI() # FastAPI 어플리케이션 객체 생성 (형식) 객체명 = 클래스명())
 
#3.접속->Get방식(=SQL select에 해당)
@app.get("/")  #HTTP GET 요청명령어 "/" 로 요청 =>함수로 만들어서 호출 
def read_root(): #FAST API =>접속=>결과물을 반환(json형태(key,value))
    return {"message": "Hello FastAPI" }

#FAST API  !=  REST API(GET,POST+PUT,DELETE)
#@app(어플리케이션객체명).요청방식명(get()):데이터를 조회할때
#@app.post() :데이터를 생성할때 (= insert)
#@app.put() :데이터를 수정할때 (= update)
#@app.delete() :데이터를 삭제할때 (= delete)
# 서버가동시키는 방법 ->uvicorn "파이션파일명(1):app객체명" --reload (=새로 고침기능)
# 서버 종료=>ctrl+c(콘솔창에서 ) 파이썬파일명_n