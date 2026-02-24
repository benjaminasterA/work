#ex2.py=>자료형->데이터의 종류,크기를 지정해주는것

print('변수선언시 대,소문자구분 조심')
print('들여쓰기 조심(함수작성시,제어문작성시,클래스작성)')#함수,메서드의 차이점

#예약어=>파이썬에서 이미 사용되고 있는 단어->변수X 
import keyword
print('키워드목록',keyword.kwlist)#암기X 
print('\n\n')#enter 2번
#자료형=>내장함수=>파이썬을 설치하면 자동적으로 내부적으로 존재하는 함수<->사용자 정의 함수
# oct(숫자)=>8진수, hex(숫자)->16진수,bin(숫자)->2진수
print(10,oct(10),hex(10),bin(2))#10 0o12 0xa 0b10
print('파이썬의 자료형')

print(7,type(7))#type(자료형)->문자,숫자,불변수,,, 7 <class 'int'>
print(7.2,type(7.2))#7.2 <class 'float'>
print(7+4j,type(7+4j))#(7+4j) <class 'complex'> =>복소수
print(True,type(True))#True <class 'bool'>(둘중의 하나값을 기억) =>자바에서 boolean
print('a',type('a')) #a <class 'str'>
print("a",type("a")) #a <class 'str'>
print('특별한 자료형2')
print('list,tuple,set,dict')#list ,dict
print('[1,]',type([1,]))#list  [] [1] <class 'list'>
print('(1,)',type((1,)))#tuple () (1) <class 'int'> => <class 'tuple'> (1,)
print('{1,}',type({1,}))#set {} =>set() => {1,} <class 'set'>
print({'key':1},type({'key':1}))#dict=>키명:저장할값  {} ->{'key': 1} <class 'dict'>