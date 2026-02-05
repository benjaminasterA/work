import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)
print("모델 정보=>", model)

# 2. 프롬프트(Prompt) 정의
prompt1 = ChatPromptTemplate.from_template("{item}을 활용한 혁신적인 미디어콘텐츠 아이디어 하나를 제안해줘.")
prompt2 = ChatPromptTemplate.from_template("다음 아이디어의 예상 되는 기술적 문제점 2가지를 알려줘.")
# 사용자 입력을 받을 템플릿을 생성하고 변수 'prompt'에 할당함

# 3. 체인(Chain) 생성 및 실행
chain1 = prompt1 | model | StrOutputParser()
chain2 = prompt2 | model | StrOutputParser()

idea = chain1.invoke({"item": "홀로그램"})
print("아이디어:\n", idea)

problems = chain2.invoke({"idea": idea})
print("예상 문제점:\n", problems)