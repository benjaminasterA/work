# os(오에스) 운영체제 인터페이스를 사용하여 파일 경로를 제어하기 위한 모듈 임포트
import os
import whisper

# (pip install openai-whisper)
# whisper.load_model(위스퍼 로드 모델) 함수를 사용하여 'base' 크기의 모델 객체 생성
# .to("cuda")(투 쿠다) 메서드로 GPU(지피유) 가속 연산을 활성화하여 처리 속도 향상
# (NVIDIA GPU 환경이 아닐 경우 이 부분은 주석 처리하거나 제거해야 함)
model = whisper.load_model("base") 

# os.path.abspath(__file__)(오에스 패스 앱스패스)로 현재 실행 중인 파일의 절대 경로 획득
# os.path.dirname(오에스 패스 디렉토리네임)으로 해당 파일이 포함된 폴더 경로 추출
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# os.path.join(오에스 패스 조인)을 사용하여 현재 폴더 내 'audio' 폴더의 '1.mp3' 절대 경로 생성
# (결과 예시: c:\workAI\work\LangChain\4.Multi-Model-Rag\audio\1.mp3)
audio_path = os.path.join(BASE_DIR, "audio", "1.mp3")
# 생성된 오디오 파일의 전체 경로를 콘솔 창에 출력
print(audio_path)

# model.transcribe(모델 트랜스크라이브) 메서드를 호출하여 오디오 파일을 텍스트로 변환
# (내부 알고리즘이 음성을 분석하여 언어 데이터를 추출함)

result = model.transcribe(audio_path)
# 변환 결과 딕셔너리(Dictionary) 객체에서 'text' 키에 해당하는 데이터만 추출
text = result["text"]
# 최종적으로 변환된 텍스트(text) 내용을 화면에 출력
print(text)