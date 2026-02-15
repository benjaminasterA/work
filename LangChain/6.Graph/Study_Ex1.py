from callfunction import ChatOpenAI,PromptTemplate

# 다른 모듈
from langchain.chains import ConversationChain #대화흐름을 관리하는 체인
#1.추가
from langchain.memory import ConversationSummaryMemory #대화 요약 메모리 모듈

#2.모델 설정(안정적인 gtp-4o-mini)
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.7)# 

#3.요약 메모리 설정:대화내용을 요약해서 기억하며 이전 맥락을 파악하게 한다.
memory = ConversationSummaryMemory(llm=llm)

#4.프롬프트 정의
template = """당신은 AI 여행 비서 '트래블 GPT'입니다.
이전 대화에서 나눈 도시와 활동들을 요약된 기록 ({history})을 통해 파악하고 다음 물음에 답하세요.

[제약조건]
- 답변 시작시 반드시 "이전 여행 내용을 바탕으로 추천드리면..." 문구를 포함할 것.
- 부산 -> 여수 ->강릉으로 이어지는 동선을 고려하여 테마(가족/커플/힐링)에 맞는 제안을 할것.

사용자:{input}
AI:"""

# 프롬프트 설계(1.input_variables=[,,한개이상의 키이상],template=변수대입
prompt = PromptTemplate(input_variables=["history","input"],template=template)

#5.대화체인 생성:LLM,메모리,프롬프트를 =>하나   | | | =>ConversationChain
conversation = ConversationChain(
    llm = llm,
    memory = memory,
    prompt = prompt,
    verbose = False # True=>요약과정 등 내부 로그를 볼 수 있다.
)
# --- 시나리오 기반 대화 실행 (처음부터 1.이전 대화를 기억+2.요약하면서 이전대화를 기억하라.)---

# [첫 번째 도시: 부산]
print("사용자: 이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.")
#predict=>요약하는기능(내부적)
res1 = conversation.predict(input="이번 주말엔 부산 갈 건데 가족 여행지 좀 추천해줘.")
print(f"AI: {res1}\n")#요약을 하면서 가진상태

# [두 번째 도시: 여수] - 이전 '부산 가족 여행' 맥락 유지
print("사용자: 이번엔 여수로 가볼까?")
res2 = conversation.predict(input="이번엔 여수로 가볼까?")
print(f"AI: {res2}\n")

# [세 번째 도시: 강릉] - 부산, 여수 경험을 종합한 제안
print("사용자: 그럼 마지막은 강릉이 좋을까?")
res3 = conversation.predict(input="그럼 마지막은 강릉이 좋을까?")
print(f"AI: {res3}")


    
    






