'''
func2.py파일 작성
사용자정의 함수=>만들어서 호출할 목적
          ㄴ작성이유=>필요로하면 언제든지 사용(=호출)(=재사용성)=>소스코드 줄여주는 효과
'''

#1.매개변수 X   반환값 X ->단순하고 반복적인 일을 할때

print('테스트1')
print('테스트1')
print('테스트1')
print('테스트1')
print('테스트1')

def printTest():
    print('테스트1')
    print('테스트1')
    print('테스트1')
    print('테스트1')
    print('테스트1')

#함수명()
printTest()#호출
printTest()
printTest()

print('===========================')
# 함수선언
def printTest2():
    for i in range(1,6):#1,6-1
        print('테스트'+str(i))

printTest2()#수동

#2.매개변수 O , 반환값 X =>입력을 받아서 저장,조회,계산,,,

def printTest3(start,end): #매개변수명:자료형,,,->반환값
    for i in range(start,end+1):#1,99+1=100
        print('테스트'+str(i))

printTest3(1,100)
'''
...
테스트97
테스트98
테스트99
테스트100
'''
#3.매개변수 O  반환값 O =>웹프로그래밍에서 많이 사용,수업나갈때도 많이 사용(=클래스에서 생성자(=함수))
def DoFunc(arg1,arg2):
    re = arg1+arg2
    return re    # return arg1+arg2(수식) or 객체  return [1,2,3],,,

# 반환받는 자료형 = 함수명(=생성자)(매개변수,,,,)
cal = DoFunc(10,20) #30X
print('cal(반환)=>',cal)#cal(반환)=> 30
# su=sum([30,40])
#print(sum([30,40]))
print(DoFunc(40,50))#90
print('함수명은 객체의 주소이다.',DoFunc)# <function DoFunc at 0x000001A21A03F910>
#내가 만든 함수를 다른  함수가 대신 호출->사용

otherFunc = DoFunc #주소가 공유->일을 동일하게 한다.

print(otherFunc(90,100))#임시로 대신 일을 맡기는 형태 (190)
#내장함수 globals() =>만들어진 함수 뿐만 내장함수의 정보를 출력
print('현재 객체 목록=>',globals())
#Any =>명확한 자료형이 없는 형태(=임의의 자료형)(ex 형태없는 물)

#함수의 매개변수=>갯수별로 작성해야 하는가? 보통 그렇다.(y)
# *매개변수명 =>list,set,tuple형태의 자료형을 받아서 처리
# **매개변수명 => dict

def ListMap(*ar):
    print(ar)

list=[1,3,5]; list2=[1,2,6]

ListMap(list,list2)#([1, 3, 5], [1, 2, 6])
'''
현재 객체 목록=> {'__name__': '__main__', '__doc__': 
'\nfunc2.py파일 작성\n사용자정의 함수=>만들어서 호출할 목적\n     
ㄴ작성이유=>필요로하면 언제든지 사용(=호출)(=재사용성)=>소스코드 줄여주는 효과\n',
'__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader
object at 0x000001EE8C47C550>, '__spec__': None, '__annotations__': 
{}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 
'c:\\workAI\\work\\python\\5.func\\func2.py', '__cached__': None, 
'printTest': <function printTest at 0x000001EE8C4CF7F0>,
'printTest2': <function printTest2 at 0x000001EE8C4CEB90>,
'printTest3': <function printTest3 at 0x000001EE8C4CF880>, 
'DoFunc': <function DoFunc at 0x000001EE8C4CF910>, 
'cal': 30, 'otherFunc': <function DoFunc at 0x000001EE8C4CF910>}
'''