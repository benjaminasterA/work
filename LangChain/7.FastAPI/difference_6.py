# BaseModel을 사용하는 이유 vs TypedDict을 사용하는 이유(차이점)
from fastapi import FastAPI 
from pydantic import BaseModel #데이터 검증 및 스키마 정의용(=DB)
#추가
from typing import TypedDict

#Pydantic BaseModel : 1.런타임 검증,직렬화(메모리값->파일저장(usb)(이동이 가능))
class UserModel(BaseModel): 
    username: str
    age: int = 20 #2.기본값 가능 (멤버변수에 미리 값을 저장시켜줄 수 있다.) 3.변환기능 O
   
#TypedDict: 정적 타입을 checking, 1.런타임 검증 없음=>그냥 패스할 수도 있다.
class UserTypedDict(TypedDict): #2.기본값 설정 기능X 3.실행상태에서 변환X
    username: str               # 값을 저장시킬때 반드시 그 자료형의 형에 맞게 데이터를 넣어달라
    age: int = 25 #2.기본값 기능X
    
#테스트 코드
print("====BaseModel 객체 생성 예제===")
try:
    # user1 = UserModel(username="alice") (1) 기본값 자동 적용
    user1 = UserModel(username="alice",age="25")
    print("user1:",user1)
    print("dict:",user1.model_dump())#model_dump() =>BaseModel 객체를 Python dict으로 변환

except Exception as e:# e 별칭
    print("에러발생(e)=>",e)
    
print("==\n==TypedDict 객체 생성 예제===")    

user2: UserTypedDict = {"username":"bob","age":25} #user2: {'username': 'bob', 'age': 25}
# user2: UserTypedDict = {"username":"bob"}   
print("user2:",user2)
print("age 타입",type(user2["age"]))#정수만 저장이 되어야 하는데 변환X  KeyError: 'age'
    
'''
====BaseModel 객체 생성 예제===
user1: username='alice' age=20
dict: {'username': 'alice', 'age': 20}

user1: username='alice' age=25 =>기본값을 저장해도 새로운값을 저장 O 문자열->정수형으로 변환이 된다.
dict: {'username': 'alice', 'age': 25}

==TypedDict 객체 생성 예제===
user2: {'username': 'bob'} =>기본값을 저장시켜도 반영X (기본값 지정이 안된다.)

user2: {'username': 'bob', 'age': '25'}
age 타입 <class 'str'>
'''