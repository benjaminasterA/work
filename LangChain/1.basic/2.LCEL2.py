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
prompt = ChatPromptTemplate.from_messages([
  ("system", " 너는 번역가이야, 입력 되는 한국어를 자연스러운 영어로 번역 해줘."),
  ("user", "{input}")
])
# 사용자 입력을 받을 템플릿을 생성하고 변수 'prompt'에 할당함

# parser = StrOutputParser()->

chain = prompt | model | StrOutputParser() # <-- 수정된 부분
print("체인 정보=>", chain)

result = chain.invoke({"input": "랭체인을 배우는것은 쉽고 재미있다!"})
print("최종 결과=>", result)