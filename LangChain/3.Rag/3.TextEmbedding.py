#txt,pdf파일 불러오기
from langchain_community.document_loaders import PyPDFLoader

#2.파이썬의 상대경로를 통해서 불러오는 방법
import os

print(f"현재 파이썬이 위치한 곳 {os.getcwd()} ")#work
#pdf_path = os.path.join(current_dir,"data","Samsung_Card_Manual_Korean_1.3.pdf")
os.chdir("C:/workAI/work/LangChain/3.Rag")# \ =>/로 변경
loader = PyPDFLoader("./data/Samsung_Card_Manual_Korean_1.3.pdf")
print(f"현재 파이썬이 위치한 곳2 {os.getcwd()} ")
'''
현재 파이썬이 위치한 곳 C:\workAI\work 
현재 파이썬이 위치한 곳2 C:\workAI\work\LangChain\3.Rag ggg
'''

#loader = PyPDFLoader(pdf_path)#(2)
#2.페이지별로 문서 로드
pages = loader.load()

print('자료형=>',type(pages)) #type(변수명(=객체명))
print(f"총페이지 수=>: {len(pages)}쪽")
print(f"1페이지 미리보기: {pages[0].page_content[:500]}") #슬라이싱 첫페이지의 500자만 출력

#기능2
from langchain_text_splitters import RecursiveCharacterTextSplitter #텍스트 분할도구
#chunk_size=500(문자토막의 크기)500(문자수)  chunk_overlap=50=>문맥 연결을 위해 겹치는 부분
splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)#1200->0-500 ,450-1000,1000-1200

#문서를 chunk으로 나눔
docs=splitter.split_documents(pages)
print(f"쪼개진 문서 조각의 수: {len(docs)}개")#9개

#기능3->문자열을 숫자로 바꾸는 작업(=벡터화)
import dotenv
dotenv.load_dotenv()

from langchain_openai import OpenAIEmbeddings #문자열을 숫자로 바꿔주는 역할(클래스)

embeddings = OpenAIEmbeddings() #OpenAI 임베딩 모델생성=>메서드가 필요

vector = embeddings.embed_query("인공지능 에이전트란 무엇인가요?")
print(f"변환된 숫자 벡터 길이: {len(vector)}")#변환된 숫자 벡터 길이: 1536 



