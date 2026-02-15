#1.import
import whisper #음성
from sentence_transformers import SentenceTransformer #멀티 모달 임베딩 모델 로드(텍스트/이미지+벡터)
from PIL import Image #이미지 파일 열기용
import faiss #벡터 검색 라이브러리 
import numpy as np # 배열 변환용(FAISS 필수)
import os

#AI에게 요청
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

#2.음성 데이터 처리=>(음성을 텍스트로 변환)
whisper_model = whisper.load_model("base")#Whisper 모델로드 (=load_audio (X))
# v_변수명
#path="c:\~"
#변수인데 대문자 => 파일경로,전체소스코드에서 자주 사용되는 상수값을 저장시킬목적(=정적 변수명)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))#절대경로의 파일이 위치->폴더명을 반환
audio_path = os.path.join(BASE_DIR,"audio","cat.mp3")
print(audio_path)#

#음성->텍스트로 변환->AI한테 전달->AI 처리(STT (Speech to Text))
speech_result = whisper_model.transcribe(audio_path)# ./audio/1.mp3
speech_text = speech_result["text"].strip() #1.변환된 텍스트 추출 (2.양쪽여백 제거) "show me the cat information"
print(f"[음성 인식 내용]: {speech_text}")


#3.지식창고(데이터베이스) 구축
clip_model = SentenceTransformer("clip-ViT-B-32")

#텍스트 기반 지식들을 리스트 형태로 준비
documents = [
    "Information: This is a domestic cat sitting comfortably.", # 고양이에 대한 설명
    "Information: There is a golden retriever dog in the yard.", # 강아지에 대한 설명
    "Concept: AI and Machine Learning technologies.",           # AI 기술 설명
    "Concept: Retrieval-Augmented Generation (RAG) system."      # RAG 시스템 설명
]
#준비한 문장들 512차원의 숫자배열(=벡터)로 변환
text_vectors = clip_model.encode(documents).astype("float32")

#4.작업 디렉토리
os.chdir("C:/workAI/work/LangChain/4.Multi-Modal-Rag")
print('os.getcwd()=>',os.getcwd()) #현재위치

#5.CLIP 멀티 모달 모델 로드
image_path = "./images/cat.jpg"
image = Image.open(image_path).convert("RGB")#RGB변환
image_vector = clip_model.encode([image]).astype("float32")#images 자체가 리스트객체이기 때문에 [] 사용X

################################################################
#6.FAISS 인덱스 생성=>인덱스=>데이터가 많을때 북마크역할(정렬(ㄱ~ㅎ))
dimension = text_vectors.shape[1] #모델 출력 차원 자동 추출(512)
index = faiss.IndexFlatL2(dimension) # L2 거리 기반 인덱스 생성
index.add(text_vectors)#텍스트 먼저 올리고
index.add(np.array(image_vector).astype('float32'))#numpy float32 배열 =>고속배열 연산할때   [[]]

#7.연관 정보 찾기(Retrieval)=>사용자의 음성 질문(텍스트)을 검색을 위해 숫자 벡터로 변환
query_vector = clip_model.encode([speech_text]).astype("float32")
#질문과 가장 닮은 상위 3개의 정보를 창고에서 찾는다.(거리값과 번호받음)
distances,indices = index.search(query_vector,k=3)

#검색된 결과를 사람이 읽을 수 있는 텍스트로 변환하여 담을 리스트
retrieved_contents= []
for idx in indices[0]:#가장 최근에 찾은값 [0]
    if idx < len(documents):# 찾은 번호가 0~3번 사이면 해당 텍스트 정보를 그대로 가져온다. 0~3 < 4  4<4
        retrieved_contents.append(documents[idx]) #0~3
    elif idx == len(documents): #4==4
        #찾은 번호가 4번(이미지)이라면 ,이미지를 설명하는 구체적인 텍스트를 추가한다.
        retrieved_contents.append("Visual Data: A high-resolution photo of a cat from 'cat.jpg'.")
#찾아낸 여러정보들을 줄바꿈으로 (\n)으로 연결해 하나의 참고 자료
context_text = "\n".join(retrieved_contents) # 파이썬->문자열도 객체    test="abc   "  ->test.strip() 
#                                                                         "abc   ".strip()~도 가능
print(f"[검색된 관련 정보]:\n{context_text}")
#####################################################################################
#8.지능형 답변 생성(Generation) =>GPT에게 줄 지침서(프롬프트)
template = """
당신은 멀티모달 정보를 처리해주는 전문가 AI 입니다.
제공된 [Context]에는 텍스트 정보뿐만 아니라 이미지 파일에 대한 설명(Visual Data)도 포함되어 있습니다.
사용자의 질문인 [Question]과 가장 연관성이 높은 정보를 [Context]에서 찾아 상세히 답변해 주세요.

[Context]:
{context}

[Question]:
{question}

Answer:
"""
#텍스트 템플릿을 랭체인이 사용할 수 있는 형식으로 변환
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
chain = prompt | llm | StrOutputParser()
#파이프 라인(chain)
final_answer = chain.invoke({
    "context":context_text, #위에서 검색한 참고 자료들
    "question":speech_text #사용자의 원래 음성 질문
})
print("-" * 50)
print(f"[최종 답변]:\n{final_answer}")


