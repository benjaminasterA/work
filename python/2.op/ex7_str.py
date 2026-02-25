#ex7_str.py
#문자열 String =>순서를 갖는다.
#    01234567
s = 'sequence' #문자열은 객체이다.
print(type(s)) #<class 'str'>
#''.count()  객체를 생성하는 이유=>1.데이터 저장(검증) typedDict  2.메서드 호출=>객체명.메서드명(~)
print('길이(=크기):',len(s))#8 #내장함수(=범용)
print('포함횟수:',s.count('e'))#3
print('검색위치:',s.find('e'),s.find('e',3),s.rfind('e'))#1 =>맨 첫번째만 찾아줌
#s.find(찾을 문자열,검색하는 시작위치인덱스)#검색위치: 1 4 7