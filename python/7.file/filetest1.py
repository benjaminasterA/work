#7.file->filetest1.py
'''
파일을 불러오고 또는 파일저장,파일내용을 조회->file io기능
예외처리 =>오류가 발생이 될 가능성이 있는 문장존재 ->try~except구문으로 처리
'''
import os #파일의 경로

try:
    #불러오는 구문,저장,조회(에러발생 가능성있는 구문)...
    #1.파일객체 = open('경로포함파일명','모드(r,w,rw)',encoding='utf-8')
    current_dir = os.path.dirname(os.path.abspath(__file__))#~7.file
    #text_path = os.path.join(current_dir,"data","ftest.txt")
    text_path = os.path.join(current_dir,"ftest.txt")
    print('text_path=>',text_path)
    f = open(text_path)#r
    print(f.read())#라인수를 모를경우
    f.close()#메모리 해제->가비지켈렉터
    #파일 저장
    text_path2 = os.path.join(current_dir,"ftest2.txt")
    letter = open(text_path2,mode = 'w')
    letter.write('My friend2!')
    letter.write('file Writing Testing...')
    letter.close()
    print()
    #생성된 파일 불러오기
    f2 = open(text_path2)
    #print(f2.read())#여러줄 읽어들일때 사용
    print(f2.readline())#한줄 읽어들일때 사용 My friend2!file Writing Testing...
    f2.close()
    print()#줄바꿈
    f = open(text_path)
    #3줄을 한줄씩 읽어들여서 출력
    for a in range(3):#0,1,2
        line = f.readline()
        print(line)
    f.close()
    print('==부분행 읽기,슬라이싱==')
    f = open(text_path)
    lines = f.readlines()#['My friend!\n', 'Have a good time!\n', 'hello~']
    print(lines)

except Exception as e: #except 예외처리클래스명 as 예외객체명
    print('파일처리에러발생=>',e)#발생이유
'''
text_path=> c:\workAI\work\python\7.file\ftest.txt
My friend!
Have a good time!
hello~
'''

