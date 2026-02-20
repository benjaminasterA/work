'''
7.FastAPI
   ㄴ협업 시스템=>유지보수가 편리(기능별로 파일을 분리)
    
     DB연동=>1.init_db.py(테이블생성->데이터를 저장(insert 구문))
            2.database.py=>get_db_connection()
            3.routers/users =>CRUD 작업
                     /items
                      ,,,
            4.main.py->routers/users 연결구문
            
            프로젝트 구성=>어디까지 만들것인가? 업무분석=>팀원 기능별로 할당
 init_db.py
'''
import sqlite3 #SQLite 모듈
#절대경로=>~.db(ex test.db) =>mysql=>create database test(데이터베이스명(=폴더)) ->파일(=테이블)
import os 

#대문자로 된 변수=>경로저장(정적변수)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #c:\workAI\work\LangChain\7.FastAPI
# + BASE_DIR\test.db                                                             ㄴdata -test.db
# DB_PATH = os.path.join(BASE_DIR,"data","test.db") data폴더밑에 test.db가 생성
DB_PATH = os.path.join(BASE_DIR,"test.db")#중간에 서브폴더가 없는 경우 ~7.FastAPI -  test.db
#                  +
#DB 작업=>1.실행시킬 프로그램을 가동=>Connection(연결 객체) 얻어오기
conn = sqlite3.connect(DB_PATH)# 7.FastAPI (test.db)파일 이름으로 DB생성하겠습니다.
print('conn=>',conn)#conn=> <sqlite3.Connection object at 0x000001B968CC2040>(주소값 출력)객체생성(메모리 공간생성)

#2.원하는 SQL구문을 작성한다.=>cursor객체가 필요=>sql구문을 사용할 수가 있다.
cursor = conn.cursor() #객체가 생성하는 이유 =>객체명.호출할 메서드명()
print('cursor=>',cursor) #커서객체 생성->sql구문을 사용하게 만들어주는 도구

#sql구문 create table 생성할테이블명=>제약조건 =>테이블생성,insert,update,delete,select
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
) """)
#샘플 데이터 입력(insert into 테이블명 values(입력값,,,'a',23))=>필드갯수만큼 입력
# 형식) insert into 테이블명 (필드명,필드명2) values(값1,값2,,,)
cursor.execute("INSERT INTO users(name,email) VALUES('John','john@test.com')")
cursor.execute("INSERT INTO users(name,email) VALUES('Alice','Alice@test.com')")
cursor.execute("INSERT INTO users(name,email) VALUES('Bob','bob@test.com')")

#저장하라
conn.commit() #커밋(데이터 저장)=>실제 테이블에 저장(카드 승인)<-->conn.rollback()(카드결재 취소)
conn.close() # 연결해제(메모리 해제)

print("DB Initialized!",DB_PATH)#절대경로에서 만들어졌는지 확인
'''
conn=> <sqlite3.Connection object at 0x000002D7E5742040>
cursor=> <sqlite3.Cursor object at 0x000002D7E587D140>
DB Initialized! c:\workAI\work\LangChain\7.FastAPI\test.db
'''










