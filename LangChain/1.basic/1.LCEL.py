import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
print("모델 정보=>", model)

# 2. 프롬프트(Prompt) 정의
prompt = ChatPromptTemplate.from_template("{topic}에 대해 짧게 설명해줘.")
# 사용자 입력을 받을 템플릿을 생성하고 변수 'prompt'에 할당함

parser = StrOutputParser()

chain = prompt | model | parser
print("체인 정보=>", chain)

result = chain.invoke({"topic": "랭체인"})
print("최종 결과=>", result)