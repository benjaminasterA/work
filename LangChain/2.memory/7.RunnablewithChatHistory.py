# 1️. 환경 변수 로드
'''
from dotenv import load_dotenv  # .env 파일을 읽어 환경변수 등록
load_dotenv()  # .env 파일에 있는 OPENAI_API_KEY를 환경변수로 로드
from langchain_openai import ChatOpenAI  # OpenAI 모델을 LangChain에서 사용하기 위한 래퍼

'''
from callfunction import *

# 2️. LangChain 관련 모듈 import
from langchain_core.chat_history import InMemoryChatMessageHistory  # 메모리 저장 객체 (세션별 대화 기록 저장)
from langchain_core.runnables.history import RunnableWithMessageHistory  # 세션별 대화 기록을 관리하는 래퍼
from langchain_core.messages import HumanMessage  # 사용자 메시지를 표현하는 객체

# 3️. 모델 초기화
model = ChatOpenAI(model="gpt-4o-mini")  # 사용할 OpenAI 모델 지정

# 4️. 세션 저장소 생성
store = {}  # 세션별 대화 기록을 저장할 딕셔너리

# 5️. 세션별 history 반환 함수 (매개변수 O  반환값 O ->세션 id값에 대한 데이터를 조회하고 있으면 꺼내와라)
def get_session_history(session_id: str): #(String session_id) 파이썬 매개변수명:자료형
    # 세션이 없으면 새로 생성
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()  # 새로운 메모리 객체 생성
    return store[session_id]  # 해당 세션의 메모리 반환

# 6️. RunnableWithMessageHistory 적용
with_message_history = RunnableWithMessageHistory(
    model,                 # 실행할 모델
    get_session_history    # 세션별 history 반환 함수(세션값을 꺼내올 함수 지정)
)

# 7️. 실행 요청 목록 정의
requests = [
    {"session_id": "abc2", "message": "안녕? 난 테스트김이야."},  # 첫 번째 요청 (abc2 세션 시작)
    {"session_id": "abc2", "message": "내 이름이 뭐지?"},        # 두 번째 요청 (abc2 세션 이어짐)
    {"session_id": "abc3", "message": "내 이름이 뭐지?"},        # 세 번째 요청 (abc3 새로운 세션)
    {"session_id": "abc2", "message": "아까 우리가 무슨 얘기 했지?"},  # 네 번째 요청 (abc2 세션 이어짐)
]

# 8️. 일반 invoke 실행 (for문 사용)
print("\n===== 일반 invoke 실행 =====\n")

for req in requests:

    # 세션 ID 설정
    # 체인에서 실행 옵션을 담는 약속된 딕셔너리 변수(config)
    # configurable": 랭체인 내부적으로 "이 설정은 실행 시점에 동적으로 바뀔 수 있다"라고 지정된 예약어(Key)
    # "session_id": 가장 중요한 식별자=> 누가 대화하고 있는지를 구분하는 '방 번호'
    # req["session_id"]: 사용자로부터 들어온 요청(request)에서 실제 세션 ID 값을 추출하여 할당
    config = {"configurable": {"session_id": req["session_id"]}}

    # 모델 실행 (HumanMessage 객체 전달)
    response = with_message_history.invoke(
        [HumanMessage(content=req["message"])], #세션별 대화내용 전달
        config=config  #세션id값 정보 전달
    )

    # 세션 정보와 함께 출력
    print(f"[Session: {req['session_id']}]") #세션id값 출력
    print(f"User : {req['message']}") #사용자 대화
    print(f"AI   : {response.content}") #모델에서 보내준 내용출력
    print("-" * 50)

# 9️. stream 실행 예시
print("\n===== stream 실행 (abc2 유지) =====\n")

stream_config = {"configurable": {"session_id": "abc2"}}

print("[Session: abc2]")
print("User : 내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해 말해봐")
print("AI   : ", end="", flush=True)

# 스트리밍 방식으로 모델 응답 출력(한 글자씩 실시간으로 응답을 받아 출력합니다)
for chunk in with_message_history.stream(
    [HumanMessage(content="내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해 말해봐")],
    config=stream_config
):
    print(chunk.content, end="", flush=True) # 각 응답 조각을 즉시 출력

print("\n" + "-" * 50)

# 10. 현재 세션 메모리 상태 확인
print("\n===== 현재 세션 메모리 상태 =====\n")

for session_id, history in store.items():
    print(f"[Session: {session_id}]")
    for msg in history.messages:
        print(f"  - {msg.type}: {msg.content}")  # 메시지 타입(human/ai)과 내용 출력
    print("-" * 50)
