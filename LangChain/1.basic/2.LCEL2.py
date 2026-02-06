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


#prompt = ChatPromptTemplate.from_template("{topic} 에 대해서 짧게 한 문장으로 설명해줘!")#(1)
prompt = ChatPromptTemplate.from_messages([
    #("system(=role(역할))","부여할 문장")
    ("system","너는 실력이 뛰어난 번역가야,입력되는 영어를 아주 자연스러운 한국어로 번역해줘."),
    ("user","{input}")
])

#3.출력파서(=양식에 맞춰서 출력)(모델의 응답값중에서 문자열만 쏙 뽑아냄)
#parser = StrOutputParser() #parser객체생성(=Variable(변수))

#4.체인 생성(LCEL의 핵심 | =>+ 처럼(연결))  ->압력->모델(서버)->출력
#chain = prompt | model | parser  #서로 연결된 정보
chain = prompt | model | StrOutputParser() #익명객체(=이름이 없는 객체)

# result = chain.invoke({"topic":"랭체인"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
result = chain.invoke({"input":"Learning LangChain is fun and easy for everyone"})#(2)
print(f"번역결과:{result}")


