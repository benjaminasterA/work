#1.모듈
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS #벡터 저장소

from langchain_openai import OpenAIEmbeddings,ChatOpenAI #OpenAI 임베딩 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter #문서 분할
from langchain.docstore.document import Document #문서객체
#추가
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

import dotenv
dotenv.load_dotenv()

loader = PyPDFLoader("C:/workAI/work/LangChain/3.Rag/data/Samsung_Card_Manual_Korean_1.3.pdf")
pages = loader.load()
print('type(pages)', type(pages))

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

# 검색기 생성
retriever = vector_db.as_retriever(search_Kwargs={"k":3})

prompt = ChatPromptTemplate.from_template("""
당신은 삼성전자 메모리 카드 메뉴얼에 대한 전문 어시던트입니다.
다음의 참고 문서를 바탕으로 질문에 정확하게 답해주세요.

[참고 문헌]
{content}
                                         
[질문]
{question}
                                          
한글로 간결하고 정확하게 답해주세요.
""")

rag_chain = (
    {"content" :retriever, "question" : RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini",temperature=0)
)

query = "이 유틸리티는 동시에 몇개의 카드나 UFD를 인식 할수 있습니까?"
answer = rag_chain.invoke(query)

print("질문:", query)
print("답변:", answer.content)

llm_base = ChatOpenAI(model="gpt-4o-mini", temperature=0)

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

question = [
    "삼성 메모리 카드/UFD 인증 유틸리티에서 동시에 몇개의 카드나 UFD를 인식 할수 있습니까?",
    "삼성 메모리 카드/UFD 인증 유틸리티는 Bitlocker가 활성화된 장치나 포멧 되지 않은 장치를 인증할 수 있습니까?",
    "삼성 메모리 카드/UFD 인증 유틸리티에서 지원하는 운영체제(OS) 버젼은 무엇입니까?"
]

for i,q in enumerate(question,1):
    print(f"\n==질문 {i}===")
    print("Q",q)

    base_answer = llm_base.invoke(q)
    print(f"\n{RED}[일반 ChatGPT 답변]{RESET}")
    print(base_answer.content)

    rag_answer = rag_chain.invoke(q)
    print(f"\n{RED}[일반 ChatGPT 답변]{RESET}")
    print(rag_answer.content)
