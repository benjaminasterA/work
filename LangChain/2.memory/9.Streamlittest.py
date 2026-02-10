# from langchain_openai import ChatOpenAI   # OpenAI LLM 호출용 래퍼
# from langchain_core.prompts import PromptTemplate   # 프롬프트 템플릿 생성 클래스
# from langchain_core.output_parsers import StrOutputParser   # LLM 응답을 문자열로 변환하는 파서

from callfunction import *
import streamlit as st   # Streamlit 라이브러리 불러오기 (웹 앱 UI 구성용)


# --- API 키 불러오기 ---
api_key = st.secrets["OPENAI_API_KEY"]   # secrets.toml 파일에서 OPENAI_API_KEY 불러오기

# LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)   
# model="gpt-4o-mini" → 사용할 모델 이름 지정
# api_key=api_key → OpenAI API 키 전달

# 프롬프트 템플릿 정의
prompt = PromptTemplate.from_template("'{topic}' 주제에 대해 한 문장으로 설명해줘.")
# {topic} → 사용자가 입력한 주제를 변수로 치환하여 프롬프트 생성

output_str = StrOutputParser()   # LLM 응답을 문자열로 변환하는 파서 객체 생성

# LCEL 파이프라인 구성
chain = prompt | llm | output_str
# '|' 연산자 → 체인 연결 (프롬프트 → LLM 호출 → 결과 파싱)

# --- Streamlit UI 구성 ---
st.set_page_config(page_title="LangChain Chat", page_icon="💬", layout="centered")
# page_title → 브라우저 탭 제목
# page_icon → 브라우저 탭 아이콘
# layout="centered" → 화면 중앙 정렬

st.markdown("### 💬 LangChain + Streamlit 대화형 예제")
# "###" → h3 크기 제목 표시

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []   # 대화 기록 리스트 초기화

# --- 입력 처리 함수 정의 ---
def process_input():
    user_text = st.session_state["input_box"].strip()   # 입력값 앞뒤 공백 제거
    if user_text:   # 빈 문자열이 아닌 경우만 처리
        st.session_state["messages"].append(("user", user_text))   # 사용자 메시지 저장
        with st.spinner("🤖 답변을 생성하고 있습니다... 잠시만 기다려주세요."):
            result = chain.invoke({"topic": user_text})   # 프롬프트에 topic 전달 후 LLM 호출
        st.session_state["messages"].append(("ai", result))   # AI 응답 저장

# --- 입력창과 버튼 UI 구성 ---
col1, col2 = st.columns([5,1])   # 두 개의 컬럼 생성 (비율 5:1)
with col1:
    st.text_input("Topic:", placeholder="주제를 입력하세요...", key="input_box")
    # 입력창 생성 (라벨: Topic, placeholder: 안내 문구, key: session_state 키)
with col2:
    st.write("")   # 버튼을 입력창과 같은 높이에 맞추기 위해 빈 줄 추가
    st.write("")   # 한줄 더 줘야 거의 높이가 맞게 된다.
    submit = st.button("질문하기", on_click=process_input)
    # 버튼 클릭 시 process_input 함수 실행

# --- 대화 기록 출력 (말풍선 UI) ---
for role, text in st.session_state["messages"]:
    if role == "user":   # 사용자 메시지 출력
        st.markdown(
            f"""
            <div style='text-align:right; margin:10px;'>
                <div style='display:inline-block; 
                            background:#DCF8C6; padding:12px; 
                            border-radius:15px; max-width:70%; 
                            color:black;'>
                    <b style='color:#075E54;'>🙋 사용자</b><br>{text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # text-align:right → 오른쪽 정렬
        # background:#DCF8C6 → 연두색 배경
        # padding:12px → 내부 여백
        # border-radius:15px → 둥근 모서리
        # max-width:70% → 말풍선 최대 너비 제한
        # color:black → 글자 색상 검정
        # color:#075E54 → 사용자 이름 색상 (초록빛)

    else:   # AI 메시지 출력
        st.markdown(
            f"""
            <div style='text-align:left; margin:10px;'>
                <div style='display:inline-block; 
                    background:#E6E6E6; padding:12px;
                    border-radius:15px; max-width:70%; color:black;'>
                    <b style='color:#333;'>🤖 AI</b><br>{text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # text-align:left → 왼쪽 정렬
        # background:#E6E6E6 → 회색 배경
        # padding:12px → 내부 여백