#1.모듈
from langchain_community.document_loaders import PyPDFLoader #pdf를 불러오는 전문 클래스
######################################################################################
from langchain_community.vectorstores import FAISS #벡터 저장소
from langchain_openai import OpenAIEmbeddings,ChatOpenAI #OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter #문서 분할
from langchain.docstore.document import Document #문서객체
#추가
from langchain_core.runnables import RunnablePassthrough #langchain의 LCEL문법
from langchain_core.prompts import ChatPromptTemplate #LLM에게 전달할 질문형식을 정의 프롬프트 템플릿
###############################################################################################

import dotenv
dotenv.load_dotenv()

#1.PDF 로드
loader = PyPDFLoader("C:/workAI/work/LangChain/3.Rag/data/Samsung_Card_Manual_Korean_1.3.pdf")
pages = loader.load() #List[Document] 형태로 반환
print('type(pages)=>',type(pages))#~ class List<Document>

#2.일정 길이로 쪼개기(긴 텍스트를 적은 조각으로 나눠야 검색효율 좋음)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, #chunk의 최대길이
    chunk_overlap=100 #1/5
)
docs = text_splitter.split_documents(pages) #익명객체
print('docs=>',docs) #중간과정 확인->print(중간객체명 또는 변수)

#3.임베딩 모델 초기화(텍스트 문자열->숫자 벡터로 변환)
embeddings = OpenAIEmbeddings()
print('embeddings=>',embeddings)

#4.문서 조각들과 임베딩 모델을 합쳐서 FAISS 벡터 DB 생성
vector_db = FAISS.from_documents(docs,embeddings)#분리된 Document->embedding(숫자)->vector_db
print('vector_db=>',vector_db)
print("지식 창고(vecotr DB) 구축 완료!")

#############검색기(retriever)객체 생성################
retriever = vector_db.as_retriever(search_Kwargs={"k":3}) #(k=2)=>갯수를 조절(상위 3개 유사 문서 검색)

#4 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template(""" 
 당신은 삼성전자 메모리카드 매뉴얼에 대한 전문 어시스턴트입니다.
 다음의 참고 문서를 바탕으로 질문에 정확하게 답해주세요.
 
 [참고문서]
 {context}
 
 [질문]
 {question}    
 
 한글로 간결하고 정확하게 답변해주세요.                                     
""")

rag_chain = (
    {"context":retriever, "question" : RunnablePassthrough()} #입력을 question으로 받아서 retriever 검색
    | prompt
    | ChatOpenAI(model="gpt-4o-mini",temperature=0) # 창의성(X)
)
#5.질의 수행
query = "이 유틸리티는 동시에 몇 개의 메모리카드나 UFD(=USB Flash Drive)를 인식할 수 있습니까?" #예시
answer = rag_chain.invoke(query)

#6.결과 출력
print("질문:",query)
print("답변:",answer.content)#원하는 문자열만 검색

#gpt-4o-mini 모델(1.기본 지식[빨간색] vs 검색을 통한 지식을 활용(RAG)[파란색])
llm_base =ChatOpenAI(model="gpt-4o-mini",temperature=0)
#터미널 출력시 결과구분 Ansi 색상코드 설정->텍스트 색상변경
# \033->ESC(Escape) 문자를 의미 (16진수 0x1B,ASCII 제어문자)
RED ="\033[91m"  #일반 GPT 답변용 빨간색
BLUE ="\033[94m" #GPT RAG 답변용 빨간색
RESET = "\033[0m" #색상 초기화 

#테스트에 사용할 질문들을 리스트형태로 저장
question = [
    "삼성 메모리 카드/UFD 인증 유틸리티에서 동시에 몇 개의 카드나 UFD를 인식할 수 있습니까?",
    "삼성 메모리 카드/UFD 인증 유틸리티는 BitLocker가 활성화된 장치나 포맷되지 않은 장치를 인증할 수 있습니까?",
    "삼성 메모리 카드/UFD 인증 유틸리티에서 지원되는 운영체제(OS) 버전은 무엇입니까?"
]
#성능 비교를 위한 반복문
for i,q in enumerate(question,1): #start=1 or 1
    print(f"\n==질문 {i} ===")
    print("Q:",q)
    
    #-- 1.기본 ChatGtp (RAG X) 답변 =>기본 지식(모델 학습)
    base_answer = llm_base.invoke(q)
    print(f"\n{RED}[일반 ChatGTP 답변]{RESET}") #빨간색 제목 출력
    print(base_answer.content)
    
    #--2.RAG 기반 ChatGTP (RAG O)
    rag_answer = rag_chain.invoke(q)
    print(f"\n{BLUE}[RAG 기반 답변]{RESET}") #빨간색 제목 출력
    print(rag_answer.content)
    
    print("\n------------------------------------------")