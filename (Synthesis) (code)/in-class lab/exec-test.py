code_in_string = """
for i in range(10):
    print(i)
"""

'''
code_in_string에 저장된 문자열 형태의 코드를 컴파일하여
바로 실행 가능한 상태로 만들어 code_compiled에 저장
두 번째 인자: 코드를 파일로부터 읽을 때 파일 이름 기술. 그렇지 않으면 '<string>'
세 번째 인자: 여러 문장으로 구성된 코드 컴파일 시에는 'exec'
'''
code_compiled = compile(code_in_string, '<string>', 'exec')


'''
앞에서 컴파일한 코드 code_compiled를 실행
'''
exec(code_compiled)
