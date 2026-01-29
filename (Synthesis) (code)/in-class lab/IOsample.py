import sys
import io

def read_file(filename):
    fp = open(filename, "r")
    ios = IOSamples()
    index = 0
    line = fp.readline().rstrip('\n')       # 개행문자 제거

    while line:                             # 비어있는 줄에서 파싱 중단
        line = line.split(' ')              # 공백 기준으로 파싱

        if len(line) == 1 and type(line[0]) == str and line[0].lower() == '\\null':
            line = []                       # \null은 값이 없는 경우로 처리

        if index % 2 == 0:
            line = list(map(int, line))         # 문자열을 정수로 바꿈
            ios.setInput(line)

        else:
            # 출력은 정수로 바꾸지 않음 (문자열로 비교해도 되므로)
            ios.setOutput(line)

        index += 1
        line = fp.readline().rstrip('\n')   # 개행문자 제거

    return ios

class IOSamples:
    def __init__(self):
        self.input = list()
        self.output = list()
        self.pair = 0

    def setInput(self, num):
        self.input.append(num)
        self.pair += 1

    def setOutput(self, num):
        self.output.append(num)

    def toString(self):
        print('# of i/o pairs: %d' % self.pair)

        for i in range(self.pair):
            print('pair #%d, %d input: ' % (i + 1, len(self.input[i])), end='')
            for j in self.input[i]:
                print('%d ' % j, end='')
            print()

            print('pair #%d, %d output: ' % (i + 1, len(self.output[i])), end='')
            for j in self.output[i]:
                print(j + ' ', end='')
                #print('%d ' % j, end='')
            print()
        print()

def validateCode(ios, code):    
    c = compile(code, '<string>', 'exec')   # compile code to efficiently execute it multiple times

    old_stdout = sys.stdout                 # redirect stdout to stream of string
    sys.stdout = mystdout = io.StringIO()

    num_success = 0
    num_failure = 0

    for i in range(ios.pair):   # run compiled code for each i/o pair
        exec(c, None, {'input': ios.input[i]})
        output = mystdout.getvalue().split()
        #output = list(map(int, output))         # 문자열을 정수로 바꿈

        #sys.stdout = old_stdout
        #print(output, ios.output[i])
        #old_stdout = sys.stdout # redirect stdout to stream of string
        #sys.stdout = mystdout = io.StringIO()
        
        if ios.output[i] == output:
            num_success += 1
        else:
            num_failure += 1

        # empty buffer
        mystdout.seek(0)        # move access pointer to beginning of buffer
        mystdout.truncate(0)    # move end pointer to beginning of buffer, thus current length becomes 0

    sys.stdout = old_stdout     # redirect stdout back to original

    #print(mystdout.getvalue())
    #print('s/f:',num_success, num_failure)
    
    return (num_success, num_failure)


'''
given input lists
    input: 2-D numpy array, where each column represents one list of inputs
    code: code to run
run the code, generate corresponding outputs, and return the outputs
'''
def generateOutput(input, code):
    c = compile(code, '<string>', 'exec')   # compile code to efficiently execute it multiple times

    old_stdout = sys.stdout                 # redirect stdout to stream of string
    sys.stdout = mystdout = io.StringIO()

    output = list()
    
    for i in range(input.shape[1]):        
        exec(c, None, {'input': input[:,[i]].squeeze()})
        output.append(mystdout.getvalue().split())
        
        # empty buffer
        mystdout.seek(0)        # move access pointer to beginning of buffer
        mystdout.truncate(0)    # move end pointer to beginning of buffer, thus current length becomes 0
        
    sys.stdout = old_stdout     # redirect stdout back to original

    return output

'''
reformat given output, such that it can be used for training with numpy functions
    output: 2-D array, where each element is a string object
    all elements will be converted into an integer value
    length of output will become the same as that of input
'''
def reformatOutput(output, num_elements,
                   low_input_element, high_input_element):

    # make empty/true/false output distinct from integer output
    empty_element = low_input_element - (high_input_element - low_input_element)
    false_value = high_input_element + (high_input_element - low_input_element)
    true_value = false_value + 1
    
    for i in range(len(output)):
        for j in range(len(output[i])):
            if output[i][j].lower() == 'true':                
                output[i][j] = true_value
                #print("true\n")
            elif output[i][j].lower() == 'false':
                output[i][j] = false_value
                #print("false\n")
            else:
                output[i][j] = int(output[i][j])
                
        output[i].extend([empty_element] * (num_elements - len(output[i])))
        
    #print(output)        
    return output    
