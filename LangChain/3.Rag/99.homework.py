# langchain_openai 모듈에서 ChatOpenAI 클래스 임포트
from langchain_openai import ChatOpenAI
# 대화 템플릿 생성을 위한 ChatPromptTemplate 및 메시지 홀더 임포트
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 대화 요약 메모리 구현을 위한 ConversationSummaryMemory 임포트
from langchain.memory import ConversationSummaryMemory

# [요구 사항 1] ChatOpenAI(model="gpt-4o-mini") 모델 설정
# OpenAI의 GPT-4o-mini 모델을 사용하여 지능형 응답 생성
llm = ChatOpenAI(model="gpt-4o-mini")

# [요구 사항 2] ConversationSummaryMemory로 장기 대화 기억 구현
# 대화가 길어질수록 내용을 요약하여 토큰(Token) 효율성을 높이고 기억 유지
# return_messages=True를 통해 메시지 객체 형태로 기록 반환
memory = ConversationSummaryMemory(llm=llm, return_messages=True)

# [요구 사항 3 & 4] 페르소나(Persona) 및 제약 사항 설정
# 프롬프트 엔지니어링(Prompt Engineering)을 통해 시스템 역할 부여
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 AI 여행 비서 '트래블GPT'입니다. "
               "사용자의 상황에 맞는 최적의 루트를 설계해야 합니다. "
               "답변 시 반드시 '이전 여행 내용을 바탕으로 추천드리면...'이라는 문구를 포함하세요. "
               "이전 도시의 활동을 기억하고 연결된 여행 루트나 테마별(가족/커플/힐링) 추천을 제안하세요."),
    # 대화 기록(history)이 동적으로 삽입될 위치 지정
    MessagesPlaceholder(variable_name="history"),
    # 사용자의 현재 질문이 입력될 위치
    ("human", "{input}"),
])

# 프롬프트와 LLM을 연결하여 실행 체인(Chain) 생성
chain = prompt | llm

# 테스트를 위한 대화 시나리오 입력 데이터 구성
inputs = [
    "이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.",
    "이번엔 여수로 가볼까?",
    "그럼 마지막은 강릉이 좋을까?"
]

# 사용자 입력 리스트를 순회하며 챗봇 실행
for user_input in inputs:
    # memory 객체에서 현재까지 저장된 대화 요약본(history)을 로드
    history = memory.load_memory_variables({})["history"]
    
    # 체인을 호출(invoke)하여 AI 응답 생성
    # input 키를 통해 사용자의 현재 발화를 전달
    result = chain.invoke({"history": history, "input": user_input})
  
    # 결과 출력 (사용자 발화와 AI의 응답 내용 표시)
    print(f"\n사용자: {user_input}\nAI 응답: {result.content}")
    
    # 현재의 질문(input)과 답변(output)을 메모리에 저장하여 다음 대화 시 요약에 반영
    memory.save_context({"input": user_input}, {"output": result.content})