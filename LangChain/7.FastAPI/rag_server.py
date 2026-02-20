#1.모듈
from langchain_community.vectorstores import FAISS #벡터 저장소
from langchain_community.embeddings import OpenAIEmbeddings #OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter #문서 분할
from langchain.docstore.document import Document #문서객체

# 추가 #################################################
import requests #웹 페이지 요청을 보내주는 라이브러리
from bs4 import BeautifulSoup
#######################################################

import dotenv
dotenv.load_dotenv()

####################################################################################
url = "https://ko.wikipedia.org/wiki/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5" #웹클로링
response = requests.get(url,
                        headers={"User-Agent": "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"}
)
soup = BeautifulSoup(response.text,"html.parser")
raw_text = soup.get_text()
print('raw_text=>',raw_text)

####################################################################################

#2.일정 길이로 쪼개기(긴 텍스트를 적은 조각으로 나눠야 검색효율 좋음)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, #chunk의 최대길이
    chunk_overlap=50 #1/5
)
docs = text_splitter.split_documents([Document(page_content=raw_text)]) #익명객체
print('docs=>',docs) #중간과정 확인->print(중간객체명 또는 변수)

#3.임베딩 모델 초기화(텍스트 문자열->숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
print('embeddings=>',embeddings)

#4.문서 조각들과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs,embeddings)#분리된 Document->embedding(숫자)->vector_db
print('vector_db=>',vector_db)
print("웹 크롤링 지식 창고(vecotr DB) 구축 완료!")

#5.사용자가 질문을 던졌을때 벡터DB에서 유사문서 검색
query = "인공지능은 무엇인가요?"
search_result = vector_db.similarity_search(query,k=2)#상위 2개 결과를 반환(=최근접 이웃벡터)

#6.검색결과 출력
for i,result in enumerate(search_result,start=1): #인덱스 보통 0부터 시작을 하는데 start=1 (1부터 시작)
    print(f"\n[검색결과 {i}]")
    print(result.page_content[:300])
    
