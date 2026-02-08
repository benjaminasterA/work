# (pip install langchain-openai)
# LangChain의 핵심 모듈인 ChatOpenAI 라이브러리 임포트
from langchain_openai import ChatOpenAI
# 프롬프트 구성을 위한 ChatPromptTemplate 클래스 임포트
from langchain_core.prompts import ChatPromptTemplate
# 출력 결과 정제를 위한 StrOutputParser 클래스 임포트
from langchain_core.output_parsers import StrOutputParser

# 1. ChatPromptTemplate을 사용해 프롬프트(Prompt) 구조 설계
# 시스템 메시지에는 챗봇의 성격과 답변 형식을 구체적으로 정의
# 사용자 메시지에는 변수 {question}을 배치해 질문 전달
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 어려운 기술 개념을 요약, 중요성 설명, "
               "그리고 쉬운 비유와 예시를 들어 설명하는 AI 선생님입니다. / "
               "답변은 반드시 다음 형식을 따르세요: / "
               "1. 정의, 2. 이유(중요성), 3. 쉬운 예시."),
    ("user", "{question}")
])

# 2. ChatOpenAI 모델 연결 및 설정
# 모델명은 gpt-4o-mini, 창의성 지수(temperature)는 0.7로 설정
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# 3. StrOutputParser를 사용하여 결과값을 문자열(String)로 변환
parser = StrOutputParser()

# 4. LCEL(LangChain Expression Language) 문법으로 체인(Chain) 완성
# 프롬프트 -> 언어 모델 -> 출력 파서 순서로 데이터 흐름 연결
chain = prompt | llm | parser

# 5. 체인 실행 및 결과 출력
# invoke 메서드(method)를 사용하여 질문을 던지고 결과 확인
# 공식 Python(파이썬) 도움말에 따르면 invoke는 입력을 받아 실행하는 표준 방식
question_text = "REST API란?"
response = chain.invoke({"question": question_text})

# 최종 답변 출력
print(f"질문:",question_text,"답변: \n", response)
# print(f"답변: \n", response)








