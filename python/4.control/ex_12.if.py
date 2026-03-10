#4.control-ex_12.if.py
'''
1.순차문  - 써준 순서대로 시작하는 문 - 변수선언,연산자계산,출력문
2.제어문  - 특정 조건에 따라서 실행 O or 실행X 구문
   ㄴ if문(둘중의 하나를 체크)  for문 , while구문
   
형식)  if 조건식(관계,산술,,):
         명령1
         명령2 
      명령3 
'''
var = 2
if var>=3:#2>=3  들여쓰기 -> 다른언어의 {  }와 같다.
    #pass # {}와 비슷
    print('크다')
    print('참일때 수행')
print('계속')#순차문 (if문 X) =>계속
print()#줄바꿈
'''
계속
'''
var = 5
if var>=3:
    #pass # {}와 비슷
    print('참일때 수행')
    print('계속')
    print('3보다 크다') 
'''
참일때 수행
계속
3보다 크다
'''  
if var>=3:
    print('참일때 수행')
else:
    print('거짓일때 수행')
'''
참일때 수행
'''
#여러개 if문 ->if문내의 또다른 if문(ex 로그인 처리)
print()
money = 1000
age = 23
msg = '' #초기값->에러발생(전역의 의미)

if money >=200:
    item = 'apple' #지역변수
    if age >=30:
        msg = 'young'
#제어문내에 선언된 지역변수는 제어문 밖에서 불러다 사용X(=참조 X) reference
print('item,msg=>',item,msg)#item,msg=> apple
#NameError: name 'msg' is not defined =>변수선언X(지역변수)
print()
'''
if 조건식:
   명령1
else if 조건식: =>elif 조건식2:
   명령2
'''
jumsu = 95
if jumsu>=90:
    print('우수')
else:
    if jumsu>=70:
        print('보통')
    else:
        print('저조')
print('end2')
'''
우수
end2
'''
jumsu = 75
if jumsu>=90:
    print('우수')
elif jumsu>=70:
        print('보통')
else:
        print('저조')
print('end3')
'''
우수
end3
'''

jum = int(input('점수입력?'))#'97'->97
print(jum) #>=,<= &&,|| =>and or
# if jum>=90 and jum<=100: 정석
if 90<=jum <=100:  #응용=>잘쓰는 형태X
    grade ='우수3'
elif 70<=jum<90:
    grade = '보통3'
else:
    grade = '저조3'
#문자+숫자=>계산X->문자형태로 변환(str()<->int())
print('결과'+str(jum)+'등급='+grade)#TypeError: can only concatenate str (not "int") to str
#print('결과',jum,'등급=>',grade)  상관X

'''
삼항연산자=>변수명 = (조건식)?참문장:거짓문장 (자바또는 C언어)
       파이썬 =>변수명 = 참인명령어 if 조건식 else 거짓문장
'''
a = 3
re = a*2 if a > 5 else a+2
print('re=>',re)#5  print('re'+str(re))
# 변형 삼형연산자(튜플)
# (0번째 요소,1번째 요소)[조건식] ->조건식이 참->1번째 요소선택, 거짓->0번째 요소선택
print((a+2,a*2)[a>5])#5