# 값을 입력을 받아서 검증=>class를 통해서 검증이 가능하다.
#1.FastAPI 클래스를 가져온다.
from fastapi import FastAPI 
#추가
from pydantic import BaseModel #데이터 검증 및 스키마 정의용(=DB)

#Item(상품) =>왜 상속?(멤버변수(=데이터 저장목적)와 메서드를 상속받기 위해서(=소유권 이전)
class Item(BaseModel): #입력 데이터 구조 정의  vs=>랭그래프의 class ChefState(TypedDict):
    name: str
    price: float
    is_offer: bool = None # 둘중의 하나값을 저장( True or False) boolean
     
#2.FastAPI객체를 생성
app = FastAPI() # 
 
#3.접속=>상품구매(items) => Json형태로 받아서 반환
# 기술면접 =>용어(CRUD)
# 직렬화(메모리상에 저장된 변수값을 -->파일로 저장하는것(usb에 담는것(이동목적),메일로 전송))
# 역직렬화=>usb상에 저장된 데이터(변수)를 메모리에 loading(로딩해서 작업)

@app.get("/items/")  # 객체명.멤버변수명
def create_item(item : Item): # (item_name:str, item_price:float,is_offer:bool,,,,,,,,)
    return {"item_name": item.name,
            "item_price":item.price,
            "item_is_offer":item.is_offer} #요청경로의 숫자를 그대로 반환
#uvicorn postmodel_4:app --reload