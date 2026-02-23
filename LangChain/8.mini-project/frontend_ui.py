# --- [필수 라이브러리 임포트] ---
import streamlit as st  # 웹 UI 구성용 Streamlit
import requests, os, time, textwrap  # HTTP 요청, 시스템 접근, 시간 측정, 텍스트 줄바꿈
import pandas as pd  # 통계 및 데이터프레임 처리
from io import BytesIO  # 메모리 기반 바이너리 버퍼
from PIL import Image, ImageDraw, ImageFont  # 이미지 생성 및 텍스트 삽입
from gtts import gTTS  # 텍스트를 음성으로 변환
from langsmith import Client  # LangSmith 클라이언트 (추적 및 분석용)
from dotenv import load_dotenv  # .env 환경 변수 로드

# --- [0. 환경 변수 로드] ---
load_dotenv()  # .env 파일에서 환경 변수 불러오기

# --- [효율화 1: 리소스 캐싱] ---
@st.cache_resource
def get_langsmith_client():
    """LangSmith 클라이언트를 싱글톤으로 캐싱"""
    return Client()

@st.cache_resource
def load_global_fonts():
    """운영체제에 따라 한글 폰트 경로를 캐싱"""
    fpath = "C:/Windows/Fonts/malgun.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if not os.path.exists(fpath):
        return None  # 폰트가 없으면 기본 폰트 사용
    return fpath

# --- [전역 리소스 초기화] ---
ls_client = get_langsmith_client()  # LangSmith 클라이언트 객체
font_path = load_global_fonts()  # 폰트 경로
PROJECT_NAME = os.environ.get("LANGCHAIN_PROJECT")  # 프로젝트 이름

# --- [효율화 2: 이미지 캐싱] ---
@st.cache_data(show_spinner=False)
def create_report_image_cached(text):
    """텍스트를 이미지로 변환하고 캐싱하여 성능 최적화"""
    img = Image.new('RGB', (800, 750), color=(255, 255, 255))  # 흰 배경 이미지 생성
    draw = ImageDraw.Draw(img)  # 이미지에 텍스트 삽입 도구

    # 폰트 설정 (캐시된 경로 사용)
    try:
        font = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
        t_font = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default(); t_font = font

    # 테두리 및 제목 삽입
    draw.rectangle([20, 20, 780, 730], outline=(0, 51, 153), width=3)
    draw.text((40, 40), "AI 전문가 최종 리포트", font=t_font, fill=(0, 51, 153))

    # 본문 텍스트 삽입 (줄바꿈 처리)
    y_pos = 100
    for line in textwrap.wrap(text, width=45):
        draw.text((40, y_pos), line, font=font, fill=(40, 40, 40))
        y_pos += 30

    # 이미지 버퍼 반환
    buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return buf.getvalue()

# --- [Streamlit 페이지 설정] ---
st.set_page_config(page_title="Expert Admin V13", layout="wide")

# --- [세션 상태 초기화] ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []  # 대화 기록
if "last_ans" not in st.session_state: st.session_state.last_ans = None  # 마지막 답변
if "stats_log" not in st.session_state: st.session_state.stats_log = []  # 통계 로그

# --- [사이드바 메뉴 구성] ---
menu = st.sidebar.radio("업무 선택", ["전문가 상담실", "운영 통계 대시보드"])

# --- [메뉴 1: 전문가 상담실] ---
if menu == "전문가 상담실":
    st.title("실시간 통합 상담 센터 (Front-end Optimized)")

    # 1. 이전 채팅 내역 출력
    for role, content in st.session_state.chat_history:
        with st.chat_message(role): st.write(content)

    # 2. 사용자 질문 입력 및 처리
    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.chat_history.append(("user", prompt))  # 사용자 질문 저장
        with st.chat_message("user"): st.write(prompt)

        with st.spinner("백엔드 엔진에서 지식을 추출 중입니다..."):
            # FastAPI 백엔드에 POST 요청
            res = requests.post(f"http://127.0.0.1:8000/ask?query={prompt}")
            if res.status_code == 200:
                data = res.json()
                st.session_state.last_ans = data["answer"]  # 답변 저장
                st.session_state.chat_history.append(("assistant", data["answer"]))  # 답변 출력
                st.session_state.stats_log.append(data["stats"])  # 통계 저장
                st.rerun()  # UI 새로고침

    # 3. 답변 시각화 (이미지 + 음성)
    if st.session_state.last_ans:
        st.divider()
        col1, col2 = st.columns(2)

        # 이미지 카드 생성 및 다운로드
        with col1:
            img_bytes = create_report_image_cached(st.session_state.last_ans)
            st.image(img_bytes)
            st.download_button("이미지 저장", img_bytes, "report.png", key="btn_img")

        # 음성 변환 및 다운로드
        with col2:
            tts = gTTS(text=st.session_state.last_ans[:300], lang='ko')  # 300자 제한
            v_buf = BytesIO(); tts.write_to_fp(v_buf); v_buf.seek(0)
            st.audio(v_buf.getvalue())
            st.download_button("🔊 MP3 저장", v_buf.getvalue(), "voice.mp3", key="btn_aud")

# --- [메뉴 2: 운영 통계 대시보드] ---
elif menu == "운영 통계 대시보드":
    st.title("통합 운영 관제")

    # 통계 데이터가 있을 경우
    if st.session_state.stats_log:
        df = pd.DataFrame(st.session_state.stats_log)  # 데이터프레임 변환

        # KPI 지표 출력
        m1, m2, m3 = st.columns(3)
        m1.metric("평균 지연시간", f"{df['latency'].mean():.2f}s")
        m2.metric("총 토큰 사용량", f"{df['total_tokens'].sum():,} tkn")
        m3.metric("누적 운용비용", f"${df['total_cost'].sum():.5f}")

        st.divider()
        st.line_chart(df.set_index("timestamp")["latency"])  # 지연시간 추이
        st.dataframe(df, use_container_width=True)  # 전체 로그 출력
    else:
        st.info("통계 데이터가 없습니다.")  # 초기 상태 안내
