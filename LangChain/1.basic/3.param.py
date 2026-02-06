#모듈 불러오기 (형식) from 모듈명 import 클래스,함수->하나의 파일로 만들어서 세트(=모듈)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #대화

#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키

#1.모델 설정(안정적인 gtp-4o-mini)
# temperature=0~1 (정확성 중시=0,1에 가까울수록 창의성(무작위성)중시)
model = ChatOpenAI(model="gpt-4o-mini",temperature=0.9)# 생성자(=객체가 생성이 될때 자동으로 호출되는 함수)

#prompt = ChatPromptTemplate.from_template("{topic} 에 대해서 짧게 한 문장으로 설명해줘!")#(1)
prompt = ChatPromptTemplate.from_template("다음 뉴스 내용을 바탕으로 사람들의 클릭을 유도하는 '낚시성' 헤드라인 3개를 만들어줘:{content}")

#4.체인 생성(LCEL의 핵심 | =>+ 처럼(연결))  ->압력->모델(서버)->출력
chain = prompt | model 
news_content="애플이 새로운 AI 기능을 탑재한 아이폰 18을 내년에 출시한다고 발표했습니다."
# request(요청),response(응답)
response = chain.invoke({"content": news_content})#(2)"news_content"=>문자열
print(response.content)# 응답객체명.특정키명=>값을 불러온다. 객체생성->1.데이터 저장,2.메서드호출
#                                               객체명.속성명(get)  객체명.속성명=값 (== or =)
print('====================================')
print(response)


