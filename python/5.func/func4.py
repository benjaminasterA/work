#func4.py=>
'''
함수을 호출->매개변수(=인수)
만약에 매개변수값을 전달X =>에러유발 (디폴트 매개변수를 설정이 가능)=>전달X 적용 O
'''
#1.함수선언시 초기값을 부여
def ShowGugudan(start,end=5): #2,3
    for dan in range(start,end+1): #(2,4)
        print(str(dan)+'단 출력')
        for i in range(1,10):#[1,2,,,,9]
            print(str(dan)+"*"+str(i)+"="+str(dan*i),end=' ')
        print()

ShowGugudan(2,3)#2,3
'''
2단 출력
2*1=2 2*2=4 2*3=6 2*4=8 2*5=10 2*6=12 2*7=14 2*8=16 2*9=18
3단 출력
3*1=3 3*2=6 3*3=9 3*4=12 3*5=15 3*6=18 3*7=21 3*8=24 3*9=27
'''
print('===='*20)
ShowGugudan(3)#(3,6)=>3,4,5
print('===='*20)

#2.함수호출할때 변수를 이용해서 전달 O =>매개변수명=전달할값
ShowGugudan(start=6,end=8)
print('===='*20)
#3.매개변수명=전달할값의 순서를 변경해도 OK
ShowGugudan(end=4,start=3)
print()
#4.매개변수중에서 원하는 것만 매개변수명=값
ShowGugudan(5,end=6)
print()
#5.주의할점
#첫번째 매개변수명,두번째는 상수 불가(생략 불가)
#ShowGugudan(start=2,3)
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