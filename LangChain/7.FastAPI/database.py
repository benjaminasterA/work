#database.py

import sqlite3 #DB모듈
#test.db에 접속=>위치(절대경로)
import os

#공통모듈로 만들어서 불러옴(=효율성)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #c:\workAI\work\LangChain\7.FastAPI
DB_PATH = os.path.join(BASE_DIR,"test.db")

#연결(공통모듈로 작성할 예정)=>함수로 작성=>외부에서 불러다 사용(공통모듈)
def get_db_connection():
    conn = sqlite3.connect("test.db")#id, name, email
    # t=(1,2,3)  [1,2,3]
    # print(t[0])->1 인덱스로 데이터를 구분해서 가져오기 때문에 불편
    # t=(1,"홍길동","hong@daum.net") =>t["name"]=>홍길동
    conn.row_factory = sqlite3.Row # 데이터행=>튜플형태->dict형식으로 변환 O
    return conn # =>데이터를 튜플형태로 반환