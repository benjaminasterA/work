# ex11_dic.py파일 작성

'''
dic->사전형->키:값으로 설정
1.순서가 없다.
2.키를 가지고 조회(검색)할때 사용
3.형식)변수=dict(키=값,,,,)
변수={키:값1,키2:값2,,,,}
'''
mydic=dict(k1=1,k2='abc',k3=3.4)
print(mydic)
#실행시킬때마다 출력되는 순서가 다 다름
#{'k2': 'abc', 'k3': 3.4, 'k1': 1}
#{'k3': 3.4, 'k2': 'abc', 'k1': 1}


#{'k1': 1, 'k2': 'abc', 'k3': 3.4}
dic={'파이썬':'뱀','자바':'커피','스프링':'용수철'}
print(dic)
print(len(dic))#갯수 3
#print(dic[0]) ->인덱싱이 안된다.
#print(dic['커피'])->KeyError: '커피'
#새로운 항목을 추가 가능->객체[키명]='값'
dic['데이터베이스']='오라클'
print(dic)
#dic의 값을 삭제->del 삭제시킬 객체명
del dic['데이터베이스']
print(dic)

#{'파이썬': '뱀', '자바': '커피', '스프링': '용수철'}
#3
#{'파이썬': '뱀', '자바': '커피', '스프링': '용수철', '데이터베이스': '오라클'}
#{'파이썬': '뱀', '자바': '커피', '스프링': '용수철'}

print()
friend={'body':'테스트','test1':'테스트2','test2':'테스트3'}
print(friend)
print(friend['test1'])
#키만 모아서 출력->dic객체명.keys(),
#값만모아서 출력->dic객체명.values()
print(friend.keys())
print(friend.values())
#찾는값 in dic객체명->True,False
print('boy' in friend)
print('test1' in friend)

#{'body': '테스트', 'test1': '테스트2', 'test2': '테스트3'}
#테스트2
#dict_keys(['body', 'test1', 'test2'])
#dict_values(['테스트', '테스트2', '테스트3'])
#False
#True

print()
for k in friend.keys():
    print(k,end=':')#키:키2:키3

print()
for k in friend.values():
    print(k,end=',')#값,값2,값3

#body:test1:test2:
#테스트,테스트2,테스트3,