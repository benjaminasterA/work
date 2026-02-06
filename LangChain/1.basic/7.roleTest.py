from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI, OpenAI

import dotenv


# dotenv(도트이엔브이) 모듈의 load_dotenv 함수를 호출하여 환경 변수 로드
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키
import dotenv
dotenv.load_dotenv()

#1.
llm = OpenAI(temperature=0.5)

#구성요소
chat_prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 과학 선생님이야"),
    ("user","학생에게 {topic}을 70살 어른도 이해하기 쉽게 설명해줘"),
    ("ai","좋아요, 내가 시니어학생에게 아주 잘 설명할게요.")
])

chain = chat_prompt | llm
print("\n ChatpromptTemplate 결과:")
print(chain.invoke({"topic": "중력"}))