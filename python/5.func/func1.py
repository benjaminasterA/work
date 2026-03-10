#5.func--func1.py파일
'''
함수 - 내장함수(불러다 사용), 사용자정의 함수(ex 직원) - 만들어서 호출
'''
#print(sum(3,4))#TypeError: 'int' object is not iterable (list,set,tuple)
print(sum([3,4]),sum({3,4}),sum((3,4)))
print(bin(8))#0b1000
print(int(1.7),float(3),str(5)+'오')#'5'+'오'='5오' 1 3.0 5오

print('복수개의 리스트로 튜플을 만들기') #zip 함수=>같은 인덱스값끼리 묶어주는 역할

x = [10,20,30]
y = ['a','b','c']

for i in zip(x,y):
    print(i)
'''
(10, 'a')
(20, 'b')
(30, 'c')
'''