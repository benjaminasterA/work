from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv
load_dotenv()


# # dotenv(도트이엔브이) 모듈의 load_dotenv 함수를 호출하여 환경 변수 로드
# dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키
# import dotenv

#1.
llm = OpenAI(temperature=0.5)

#구성요소
chat_prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 여행 가이드야"),
    ("user","나는 {city}에 여행을 가고 싶어"),
    ("ai","좋아요, 내가 여행 계획을 잘 설계해서 도와 드릴게요."),
    ("user","{city}에서 꼭 가봐야 할 맛집 똔는 명소 5군데와 날씨를 알려줘.")
])

chain = chat_prompt | llm
print("\n ChatpromptTemplate 결과:")
print(chain.invoke({"city": "강화도"}))