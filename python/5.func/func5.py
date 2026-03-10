#func4.py=>
'''
함수의 매개변수 전달2(종합 *,**)
'''

print('\n가변 인수 처리')
def Func1(*ar):#list,set,tuple
    print(ar)#('ham', 'egg', 'spam')
    for i in ar:
        print('food=>'+i)
Func1('ham','egg','spam')
#주의할점
#TypeError: Func2() missing 1 required keyword-only argument: 'a'
#가변매개변수를 사용할때 다른 매개변수는 뒤에 배치X =>앞에서 전부 받아서 처리되기때문
#def Func2(*ar,a):#list,set,tuple
print('=======================')
def Func2(a,b,*ar):
    print(ar)# ('egg', 'spam')
    print(a,b)#ham
    for i in ar:
        print('food=>'+i)
        
Func2('ham','egg','spam')
#추가
print("=============추가=================")
print('\n dict 타입의 자료형')
def Func3(w,h,**other):
    print('몸무게 {},키 {} '.format(w,h))#몸무게 65,키 175
    print(other)#dict형 값 출력

#입력=>매개변수명=값,매개변수명2=값2,,, 
Func3(65,175,irum='홍길동',nai=23,sung='남',addr='대전')
#{'irum': '홍길동', 'nai': 23, 'sung': '남', 'addr': '대전'}
#TypeError: Func3() takes 2 positional arguments but 3 were given
# **매개변수=>dict형태로 출력을 하지만 전달하는 과정에서는 dict형으로 전달X
#Func3(65,175,{'irum':'홍길동2','nai':23})
Func3(75,185,irum='김길수')#{'irum': '김길수'}

print('\n 종합')
def Func4(a,b,*v1,**v2):
    print(a)# ('egg', 'spam')
    print(b)
    print(v1)#()형태
    print(v2)#{}형태

Func4(1,2)
Func4(1,2,3,4,5)#(3,4,5)=>*v1
Func4(1,2,3,4,5,m=6,n=7)#{'m': 6, 'n': 7}
'''
1
2
()
{}
1
2
(3, 4, 5)
{}
1
2
(3, 4, 5)
{'m': 6, 'n': 7}

'''