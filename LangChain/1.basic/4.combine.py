#모듈 불러오기 (형식) from 모듈명 import 클래스,함수->하나의 파일로 만들어서 세트(=모듈)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #대화
from langchain_core.output_parsers import StrOutputParser #문자형태로 출력

#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키

#1.모델 설정(안정적인 gtp-4o-mini)
model = ChatOpenAI(model="gpt-4o-mini")# 클래스->객체생성(1.데이터 저장,2.메서드호출)=>인증을 받은상태

prompt1 = ChatPromptTemplate.from_template("{item} 을 활용한 혁신적인 미디어콘텐츠 아이디어를 하나 제안해줘")
prompt2 = ChatPromptTemplate.from_template("다음 아이디어의 예상되는 기술적 문제점 2가지를 알려줘: {idea} ")
#3.출력파서(=양식에 맞춰서 출력)(모델의 응답값중에서 문자열만 쏙 뽑아냄)

#4.체인 생성(LCEL의 핵심 | =>+ 처럼(연결))  ->압력->모델(서버)->출력
chain1 = prompt1 | model | StrOutputParser()  #서로 연결된 정보 parser1
chain2 = prompt2 | model | StrOutputParser()              #   parser2    

#첫본째 실행
idea = chain1.invoke({"item":"홀로그램"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
print(f"아이디어:{idea}\n")

#첫번째 결과를 두 번째 체인의 입력값으로 사용
problems = chain2.invoke({"idea": idea}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
print(f"예상 문제점:\n{problems}")


