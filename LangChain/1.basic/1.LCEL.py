#모듈 불러오기 (형식) from 모듈명 import 클래스,함수->하나의 파일로 만들어서 세트(=모듈)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #대화
from langchain_core.output_parsers import StrOutputParser #문자형태로 출력

#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키

#1.모델 설정(안정적인 gtp-4o-mini)
model = ChatOpenAI(model="gpt-4o-mini")# 클래스->객체생성(1.데이터 저장,2.메서드호출)=>인증을 받은상태
#print("model=>",model) # 객체생성=>메모리에 공간이 잡힌다.=>주소값(=집주소)

#dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키가 나중에 전달
#2 프롬프트 설정 =>함수와 메서드 구분 (함수(=프리랜서),메서드(=함수)(기관.메서드)->소속)
#  함수명(항목,,,(=매개변수명(=함수가 처리할 값)))
#prompt = ChatPromptTemplate.from_template("{topic} 에 대해서 짧게 한 문장으로 설명해줘!")#(1)
prompt = ChatPromptTemplate.from_template("인공지능에 대해서 짧게 한 문장으로 설명해줘!")

#3.출력파서(=양식에 맞춰서 출력)(모델의 응답값중에서 문자열만 쏙 뽑아냄)
parser = StrOutputParser() #parser객체생성(=Variable(변수))

#4.체인 생성(LCEL의 핵심 | =>+ 처럼(연결))  ->압력->모델(서버)->출력
chain = prompt | model | parser  #서로 연결된 정보

# result = chain.invoke({"topic":"랭체인"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
result = chain.invoke({})#(2)
print("result=>",result)
'''
result=> 랭체인(LangChain)은 다양한 언어 모델을 활용하여 자연어 처리 작업을 쉽게 수행하고, 
복잡한 애플리케이션을 개발할 수 있도록 지원하는 프레임워크입니다.
'''

