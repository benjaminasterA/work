"""
공통 import 및 환경 설정 모듈
  이 파일을 import 하시면
  1).env 자동 로드 
  2) 필요한 클래스들을 함께 가져올 수 있음    
"""

#======환경변수 로드===============
#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()

#=====공통의 모듈을 import ============
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #대화
from langchain_core.output_parsers import StrOutputParser #문자형태로 출력
#추가
from langchain_core.prompts import PromptTemplate