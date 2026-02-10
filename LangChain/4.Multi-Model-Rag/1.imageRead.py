# (pip install langchain-openai python-dotenv)
# base64(베이스64) 이미지 인코딩을 위한 모듈 임포트
import base64
# langchain_openai(랭체인 오픈에이아이) 패키지에서 ChatOpenAI(챗 오픈에이아이) 임포트
from langchain_openai import ChatOpenAI
# 메시지 구성을 위한 HumanMessage(휴먼 메시지) 객체 임포트
from langchain_core.messages import HumanMessage
# .env 환경 변수 로드를 위한 dotenv(도트 이앤브이) 임포트
from dotenv import load_dotenv

# load_dotenv()(도트 이앤브이 로드)를 실행하여 API 키 설정 활성화
load_dotenv()

# 모델명 오타 수정: gpt-4o-min -> gpt-4o-mini (정확한 명칭 사용)
model = ChatOpenAI(model="gpt-4o-mini")

# 이미지를 base64(베이스64) 문자열로 변환하는 함수 정의
def encode_image(image_path):
    # 파일 열기: 바이너리 읽기(rb) 모드 사용
    with open(image_path, "rb") as image_file:
        # 데이터 읽기 및 인코딩 후 문자열로 변환하여 반환
        return base64.b64encode(image_file.read()).decode('utf-8')

# 이미지 파일 경로 지정 (사용자 환경에 맞게 수정 필요)
image_path = "C:/workAI/work/LangChain/4.Multi-Model-Rag/images/local_stitch_terrarosa.jpg"
image_base64 = encode_image(image_path)

# HumanMessage(휴먼 메시지) 구성 시 딕셔너리(Dictionary) 구조 및 문법 수정
# (type: text와 type: image_url의 형식을 공식 가이드에 맞춤)
message = HumanMessage(content=[
    {
        "type": "text", 
        "text": "이 사진에 대하여 기자처럼 자세히 설명을 해줘요"
    },
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}"
        }
    }
])

# model.invoke(모델 인보크)를 통해 메시지를 모델에 전달하고 응답 수신
response = model.invoke([message])

# 분석 결과(content)를 출력 (f-string 내 변수 위치 수정)
print(f"사진 분석 결과: {response.content}")