
from langchain_core.prompts import ChatPromptTemplate # 사용하는것만 기재(메모리효율성 좋다.)
from langchain_openai import OpenAI

# 라이브러리(자주 사용되는 함수,클래스,속성)=>Module(모듈)
#apikey
# import dotenv #환경변수=>import 모듈명->안에 있는 다른 함수도 불러올 수가 있다.
# dotenv.load_dotenv() # 모듈명.불러올 함수형태로 사용

from dotenv import load_dotenv 
load_dotenv()
# 모듈을 직접 만들어서 불러와서 사용(=사용자정의 모듈작성)

#1.
llm = OpenAI(temperature=0.5)# LLM 초기화

# SystetemMessage->모델의 성격,역할,규칙을 정의
# UserMessage(=HumanMessage):실제 입력값을 전달하는 부분
# AIMessage: 모델의 응답 톤이나 기본 답변 스타일을 지정

#구성요소=>System,User(=Human)Message,AI Message =>90%+10%추가
chat_prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 여행 가이드야"),#시스템 메세지 (System Message) 역할부여
    ("user","나는 {city}에 여행을 가고 싶어."), #사용자 메세지 (UserMessage)(제한적인 단어)->토큰(속도향상)
    ("ai","좋아요,여행계획을 잘 설계해서 도와드릴께요."), #AI Message
    ("user","그 도시에서 유명한 맛집과 날씨도 같이 알려줘!"),   #[] ,set {}
])

chain = chat_prompt | llm #model
print(chain.invoke({"city": "파리"}))









'''
# result = chain.invoke({"topic":"랭체인"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
user_input="오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다."
result = chain.invoke({"korean_text": user_input})#(2) 

print(f"입력:{user_input}")
print(f"결과:{result}")

'''
