#모듈 불러오기 (형식) from 모듈명 import 클래스,함수->하나의 파일로 만들어서 세트(=모듈)
# PromptTemplate,ChatPromptTemplate의 차이점
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate #대화
from langchain_openai import OpenAI

#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키

#1.
llm = OpenAI(temperature=0.5)# LLM 초기화
#print("model=>",model) # 객체생성=>메모리에 공간이 잡힌다.=>주소값(=집주소)

# ~ 찾아서 보여줘=>찾는 양이 많아서 tokens max limited =>요약해줘 또는 몇 단어이내로 간결하게 알려줘
# 단순 문자열 기반 프롬프트
prompt = PromptTemplate(
   input_variables=["topic"],#입력변수
   template="다음 주제에 대해 간단히 설명해줘:{topic}"
)

chain1 = prompt | llm
print("promptTemplate 결과:") 
print(chain1.invoke({"topic": "인공지능"}))#ctrl+s(저장)
print('==================================================')
#ChatOpenAI 객체 따로 선언 model
chat_prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 상담사야"),#시스템 메세지 (System Message)
    ("user","다음 주제에 대해 5살 어린이도 알기 쉽게 설명해줘: {topic}") #사용자 메세지 (UserMessage)(제한)->토큰(속도향상)
])

chain2 = chat_prompt | llm #model
print("\n ChatpromptTemplate 결과:") 
print(chain2.invoke({"topic": "인공지능"}))









'''
# result = chain.invoke({"topic":"랭체인"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
user_input="오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다."
result = chain.invoke({"korean_text": user_input})#(2) 

print(f"입력:{user_input}")
print(f"결과:{result}")

'''
