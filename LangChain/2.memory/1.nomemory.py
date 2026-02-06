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

# ~ 찾아서 보여줘=>찾는 양이 많아서 tokens max limited =>요약해줘 또는 몇 단어이내로 간결하게 알려줘
prompt = ChatPromptTemplate.from_template("{input}")

chain = prompt | model | StrOutputParser() #익명객체(=이름이 없는 객체)


# result = chain.invoke({"topic":"랭체인"}) # [] ,{키명:전달할값} 오타=>json형식=>데이터 전송 #(1)
user_input="오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다."
result = chain.invoke({"input": user_input})#(2)

print(f"질문1:내이름은 테스트김이야 /응답:{chain.invoke({'input': '내이름은 테스트김이야'})}")
print(f"질문2:오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다. /응답:{chain.invoke({'input': '오늘 날씨가 너무 좋아서 근처 공원에 산책을 가고 싶다.'})}")
print(f"결과:{result}")