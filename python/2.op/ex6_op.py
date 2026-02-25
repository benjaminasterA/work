#ex6_op.py

'''
연산자=>연산을 하기위한 기호(+,-,*,/,%,,,) 산술,관계연산자,논리연산자,,,
'''
#// 몫   %->나머지  ** 거듭제곱 =>산술연산자
print(5+2,5-2,5*2,5/2,5//2,5%2,5**2)#7 3 10 2.5 2 1 25
print('나누기에서 몫과 나머지를 구하기')
print(divmod(5,2))#(2,1) 몫,나머지
#관계(=비교)연산자=>True,False 반환값
print('논리연산자',end=',')
print(5>3 and 4<3,5>3 or 4<3,not(5>=3))#논리연산자,False True False
print('문자열 더하기',end=':')
print('테'+'스'+"트연습")#테스트연습
print('테스트'*100)#특정문자열*반복횟수
print('누적(할당(=배당)연산자)')
#a = a+1  =>a+=1 a++(증)   a=a-1 a--(감)  증감연산자=>파이썬에서는 없다.
a = 10
a = a + 1 #11
a+=1 #11+1=12
print(a)#12

print('부호변경',a,a*-1,-a,--a)# 12 -12 -12 12     -(-12)=12  --=>음의 기호로 사용한것.
print('bool처리',bool(0),bool(1),bool(2),bool(3),bool(None),bool(''))#False True True True False False
'''
0외에는 True 0->False, None,공백=>False
'''