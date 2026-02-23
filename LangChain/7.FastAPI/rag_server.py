#1.모듈
#rag_server.py (FastAPI 기반 RAG 서버)
from fastapi import FastAPI # 서버 프레임워크
from pydantic import BaseModel  # 요청 데이터 모델 정의용

from langchain_community.vectorstores import FAISS #벡터 저장소
from langchain_openai import OpenAIEmbeddings,ChatOpenAI #임베딩+LLM

from langchain.text_splitter import RecursiveCharacterTextSplitter #문서 분할
from langchain.docstore.document import Document #문서객체

# 추가 #################################################
from langchain.prompts import ChatPromptTemplate
import requests #웹 페이지 요청을 보내주는 라이브러리
from bs4 import BeautifulSoup
#######################################################

import dotenv
dotenv.load_dotenv()

app = FastAPI() #앱객체
#전역객체 초기화

#3.임베딩 모델 초기화(텍스트 문자열->숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
print('embeddings=>',embeddings)

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0
)


#데이타로딩 벡터 DB 생성

####################################################################################
def build_vector_db():
    url = "https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5" #웹클로링
    response = requests.get(url,
                        headers={"User-Agent": "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"}
                        )
    print('response=>', response) #디버깅

    soup = BeautifulSoup(response.text,"html.parser")
    raw_text = soup.get_text()
    print('raw_text=>',raw_text)

####################################################################################

#2.일정 길이로 쪼개기(긴 텍스트를 적은 조각으로 나눠야 검색효율 좋음)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, #chunk의 최대길이
        chunk_overlap=50 #1/5
    )
    docs = splitter.split_documents([Document(page_content=raw_text)]) #익명객체
    print('docs=>',docs) #중간과정 확인->print(중간객체명 또는 변수)
#4.문서 조각들과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
    vector_db = FAISS.from_documents(docs,embeddings)#분리된 Document->embedding(숫자)->vector_db
    print('vector_db=>',vector_db)
    print("웹 크롤링 지식 창고(vecotr DB) 구축 완료!")
    return vector_db

#서버 시작시 백터db 생성
vector_db = build_vector_db()

#요청모델 정의
class QuestionRequest(BaseModel):
    question: str

#사용자가 질문을 던졌을때 벡터DB에서 유사문서 검색
@app.post("/ask")
def ask_question(request: QuestionRequest):

    query = request.question
    print('query=>', query)
#백터유사도검색
    results = vector_db.similarity_search(query,k=3)#상위 2개 결과를 반환(=최근접 이웃벡터)
    print('result=>',results)
#검색결과 출력
    context = "\n\n". join([doc.page_content for doc in results])
    print('context=>',context)

#프롬프트구성
    prompt = ChatPromptTemplate.from_template("""
    당신은 AI 전문가입니다.
    반드시 아래문서를 참고해고 문서의 내용이 길면
    요약해서 답변해주세요.                                         
    문서에 없는 내용은 추측하지 마세요.

    문서:
    {content}
                                          
    질문:

    {question}
    """)
#체인생성
    chain = prompt | llm
    response = chain.invoke({
        "content": context,
        "question": query

    })

    return{"answer":response.content}
