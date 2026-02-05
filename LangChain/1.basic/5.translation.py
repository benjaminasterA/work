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
prompt = ChatPromptTemplate.from_template(
    "다음 한국어 문장을 영어로 번역하되, 반드시 10단어 이내로 간결하게 답해줘.\n문장: {korean_text}"

)
# 사용자 입력을 받을 템플릿을 생성하고 변수 'prompt'에 할당함

# parser = StrOutputParser()->

chain = prompt | model | StrOutputParser() # <-- 수정된 부분
print("체인 정보=>", chain)

user_inputs = "오늘 날씨가 너무 좋아서 근처 공원에서 산책하고 싶다."
result = chain.invoke({"korean_text": user_inputs})
print("입력=>", user_inputs)
print("번역 결과=>", result)