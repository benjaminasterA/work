#class3_student.py=>생성자 추가
'''
생성자
 1.파이썬에서 객체를 생성할때 자동으로 호출되는 특수한 메서드 ->임의로 호출X
   =>ex) 카드결재 O =>폰(카드내역) O  객체생성X  =>호출불가
 2.생성자명=> __init__(self) 
 3.생성자의 기능=> 데이터의 저장을 위한 초기값 설정(=처음에 저장할값)
'''
class Student:
    age= -1 #나이 설계상으로 만든 멤버변수(=속성)
    #name =>정적
    #생성자->자동호출->초기값 부여할때 사
    def __init__(self,name,age=17): #밖에서 작업 매개변수2개로 표시
        self.name = name #동적으로 멤버변수 추가 가능  self.동적으로 생성한 멤버변수=초기값
        self.age = age #s.age=17
    #저장값 불러오기
    def print_name(self):#매개변수가 없는 메서드
        print(self.name)
    
    def print_age(self):#매개변수가 없는 메서드
        print(self.age)

#s = Student()#기본생성자 호출 =>매개변수가 없는 생성자  __init__()
s = Student("철수") #Student라는 클래스를 통해서 s라는 객체를 생성하면서 자동호출된 생성자에게 
#                   철수라는 값을 전달한다.
#파이썬에서 메서드를 호출하는 방법 2가지
s.print_name() #bound method call (객체명.호출할 메서드명(~))  bound=>객체가 자동으로 전달(연결)
#원형클래스명.호출할메서드(객체명)=>객체명을 매개변수명으로 전달해서 호출=>unbound method call
Student.print_name(s)

s2 = Student("영희",23)#생성자 인수 2개
s2.print_name()  #영희 
    