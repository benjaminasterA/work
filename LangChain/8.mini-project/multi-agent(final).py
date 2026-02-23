import streamlit as st  # 웹 인터페이스 제작용 라이브러리
import os, time, base64, textwrap  # 시스템 제어, 시간 측정, 인코딩, 텍스트 줄바꿈 도구
import pandas as pd  # [추가] 통계 데이터 분석 및 표 생성을 위한 라이브러리
from io import BytesIO  # 메모리 내 바이너리 데이터 처리용 버퍼
from PIL import Image, ImageDraw, ImageFont  # 이미지 생성 및 한글 폰트 렌더링
from gtts import gTTS  # 텍스트-음성 변환(TTS) 엔진
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # OpenAI 모델 및 임베딩 연결
from langchain_community.document_loaders import PyPDFLoader  # PDF 문서 로더
from langchain_community.vectorstores import FAISS  # 벡터 검색 데이터베이스
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 텍스트 분할기
from langchain.tools import tool  # 에이전트 전용 도구 정의용 데코레이터
from langchain.agents import AgentExecutor, create_openai_functions_agent  # 에이전트 실행 엔진
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 프롬프트 설계 도구
from langchain_community.callbacks.manager import get_openai_callback  # 토큰량 및 비용 실시간 추적기
from dotenv import load_dotenv  # 환경 변수(.env) 로드 도구

# API 키 및 환경 설정 로드
load_dotenv()

# --- [1. 자원 최적화: 싱글톤 모델 및 세션 설정] ---
# 모델 객체를 매번 생성하지 않고 세션에 하나만 등록하여 공유 (토큰 및 메모리 절약)
if "shared_llm" not in st.session_state:
    st.session_state.shared_llm = ChatOpenAI(model="gpt-4o", temperature=0)

if "messages" not in st.session_state: st.session_state.messages = []  # 대화 이력 저장소
if "last_response" not in st.session_state: st.session_state.last_response = ""  # 최신 답변 저장소
if "stats_history" not in st.session_state: st.session_state.stats_history = []  # 통계 로그 저장소

DB_INDEX_PATH = "faiss_index_storage"  # 벡터 DB 저장 경로

# --- [2. 에이전트 도구 정의: 데이터 원문만 반환하여 토큰 최소화] ---

@tool
def search_allergy_docs(query: str):
    """반려동물 알레르기 PDF에서 관련 정보를 찾아 원문 문맥을 반환합니다."""
    try:
        embeddings = OpenAIEmbeddings()
        if os.path.exists(DB_INDEX_PATH):
            vector_db = FAISS.load_local(DB_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        else:
            loader = PyPDFLoader("./data/반려동물_알레르기_예방관리수칙.pdf")
            docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=30))
            vector_db = FAISS.from_documents(docs, embeddings)
            vector_db.save_local(DB_INDEX_PATH)
        
        # 에이전트가 판단할 수 있도록 검색된 원문 2개만 전달 (토큰 절약)
        results = vector_db.similarity_search(query, k=2)
        return "\n".join([f"[출처:{d.metadata.get('page')}p] {d.page_content}" for d in results])
    except Exception as e:
        return f"문서 검색 중 오류: {str(e)}"

@tool
def fetch_diabetes_raw(dummy: str = ""):
    """당뇨병 진료지침서의 핵심 요약용 원문 데이터를 가져옵니다."""
    try:
        loader = PyPDFLoader("./data/2025_당뇨병_진료지침.pdf")
        pages = loader.load()
        # 전체가 아닌 핵심 내용이 있는 앞부분 3페이지만 전송하여 비용 절감
        return " ".join([p.page_content for p in pages[:3]])
    except Exception as e:
        return f"지침서 로드 실패: {str(e)}"

tools = [search_allergy_docs, fetch_diabetes_raw]

# --- [3. 시각화 보조: 이미지 생성 함수] ---
def create_report_image(text):
    """답변 내용을 한글 깨짐 없이 PNG 이미지 리포트로 변환"""
    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    # 한글 폰트 설정 (환경에 따라 자동 탐색)
    fpath = "C:/Windows/Fonts/malgun.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    try:
        font = ImageFont.truetype(fpath, 20); t_font = ImageFont.truetype(fpath, 30)
    except:
        font = ImageFont.load_default(); t_font = font

    draw.text((40, 40), "📋 AI 분석 결과 리포트", font=t_font, fill=(0,0,0))
    y = 100
    for line in textwrap.wrap(text, width=42): # 텍스트 줄바꿈 처리
        draw.text((40, y), line, font=font, fill=(64,64,64))
        y += 30
    
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return buf.getvalue()

# --- [4. 메인 UI 및 에이전트 구동] ---
st.set_page_config(page_title="Expert Agent Admin", layout="wide")

# 사이드바 관리 메뉴
with st.sidebar:
    st.header("🎛️ 에이전트 설정")
    menu = st.selectbox("기능 전환", ["💬 전문가 상담실", "📊 운영 분석 대시보드"])
    st.divider()
    if st.button("🗑️ 모든 로그 초기화"):
        st.session_state.messages = []; st.session_state.stats_history = []; st.rerun()

# 에이전트 공통 설정 (싱글 모델 활용)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 도구가 제공한 팩트만을 근거로 답변하는 전문 위원입니다."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
agent_engine = create_openai_functions_agent(st.session_state.shared_llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent_engine, tools=tools, verbose=True)

# 메뉴 1: 상담 서비스
if menu == "💬 전문가 상담실":
    st.title("👨‍⚕️ 통합 AI 전문 에이전트")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if user_query := st.chat_input("문의 사항을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.write(user_query)

        with st.chat_message("assistant"):
            # 단일 모델 실행 시 토큰 소모량 실시간 캡처
            with get_openai_callback() as cb:
                start_time = time.time()
                # 문맥 최적화: 최근 대화 3개만 유지하여 입력 토큰 절약
                response = agent_executor.invoke({"input": user_query, "chat_history": st.session_state.messages[-3:]})
                ans = response["output"]
                latency = round(time.time() - start_time, 2)
                
                st.write(ans)
                st.session_state.last_response = ans
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
                # 통계 로그 기록
                st.session_state.stats_history.append({
                    "시간": time.strftime("%H:%M:%S"),
                    "속도": latency,
                    "토큰": cb.total_tokens,
                    "비용": cb.total_cost
                })

    # 하단 유틸리티 섹션
    if st.session_state.last_response:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 음성 브리핑"):
                tts = gTTS(text=st.session_state.last_response, lang='ko')
                fp = BytesIO(); tts.write_to_fp(fp); fp.seek(0)
                st.audio(fp, format="audio/mp3")
        with c2:
            img_data = create_report_image(st.session_state.last_response)
            st.download_button("📸 리포트 다운로드 (PNG)", img_data, "ai_report.png", "image/png", key="down_btn")

# 메뉴 2: 강화된 분석 대시보드
elif menu == "📊 운영 분석 대시보드":
    st.title("📈 시스템 운영 지표 분석")
    
    if not st.session_state.stats_history:
        st.info("아직 대화 데이터가 없습니다. 상담을 진행해주세요.")
    else:
        df = pd.DataFrame(st.session_state.stats_history)

        # [요청사항 반영] 상단 지표 영역 (KPI Metrics)
        c1, c2, c3 = st.columns(3)
        c1.metric("평균 응답 시간", f"{df['속도'].mean():.2f}초", delta=f"{df['속도'].iloc[-1] - df['속도'].mean():.2f}s", delta_color="inverse")
        c2.metric("누적 토큰 소모", f"{df['토큰'].sum():,} tokens")
        c3.metric("누적 운영 비용", f"${df['비용'].sum():.5f}")

        st.divider()

        # [시각화 강화] 처리 속도 및 토큰 소모량 그래프
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("⏱️ 응답 시간 추이 (Latency)")
            st.line_chart(df.set_index("시간")["속도"])
            st.caption("질문별 소요 시간의 변화를 보여줍니다.")

        with col_right:
            st.subheader("🪙 토큰 사용 효율성")
            st.bar_chart(df.set_index("시간")["토큰"])
            st.caption("요청당 소모된 토큰량을 비교합니다.")

        # [요청사항 반영] 상세 세션 로그 리포트 테이블
        st.subheader("📝 상세 세션 실행 로그")
        st.dataframe(df, use_container_width=True)
        
        # 비용 요약 카드
        st.info(f"💡 현재까지 총 {len(df)}건의 요청을 처리했으며, 평균 비용은 요청당 ${df['비용'].mean():.6f} 입니다.")