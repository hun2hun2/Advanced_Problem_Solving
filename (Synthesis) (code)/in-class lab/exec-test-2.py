code_in_string = """
answer = sum(i for i in input)
print(answer)
"""

'''
code_in_string에 저장된 문자열 형태의 코드를 컴파일하여
바로 실행 가능한 상태로 만들어 code_compiled에 저장
두 번째 인자: 코드를 파일로부터 읽을 때 파일 이름 기술. 그렇지 않으면 '<string>'
세 번째 인자: 여러 문장으로 구성된 코드 컴파일 시에는 'exec'
'''
code_compiled = compile(code_in_string, '<string>', 'exec')


'''
앞에서 컴파일한 코드 code_compiled를 실행하되
변수 'input'에 미리 리스트 [1, 3, 5, 7]를 저장한 상태로 코드 실행
'''
exec(code_compiled, None, {'input': [1, 3, 5, 7]})
