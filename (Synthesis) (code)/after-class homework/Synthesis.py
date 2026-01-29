import math
import random
import timeit
from pathlib import Path


NUM_INPUT, NUM_OUTPUT = 5, 5
MIN_INPUT, MAX_INPUT = -10, 10
MIN_OUTPUT, MAX_OUTPUT = -20, 20
ENCODE_EMPTY, ENCODE_TRUE, ENCODE_FALSE = -100, 100, 101
def evaluateModelWithFiles(model, paramList, fileNameList, debug):
    '''
    Evaluate the 'model' to see whether it can differentiate io-samples in 'fileNames'
    Input:
        model - function that takes 'parameters' as input argument
        paramList - list of parameter sets, where each set is used to differentiate one target
        fileNameList - list of file names, where each file contains IO samples of one target
        debug - if True, print each failure
    Output:
        list of (# of successes, # of failures) for each target
    '''
    #assert len(paramList) == len(fileNameList), f"the numbers of paramter sets ({len(paramList)}) and those of file names ({len(fileNameList)}) must be equal"

    ioSamples = []
    for fileName in fileNameList:
        filePath = Path(__file__).with_name(fileName)   # use the location of the current .py file        
        with filePath.open('r') as f:
            inputs, outputs = [], []
            lineInput, lineOutput = f.readline().strip(), f.readline().strip()
            while lineInput and lineOutput:
                inputs.append([int(i) for i in lineInput.split()])
                output = []
                for i in lineOutput.split():                    
                    #if i == "true": output.append(ENCODE_TRUE)
                    #elif i == "false": output.append(ENCODE_FALSE)
                    if i == "True" or i == "False": output.append(i)
                    else: output.append(int(i))
                #while len(output) < NUM_OUTPUTS: output.append(ENCODE_EMPTY)
                outputs.append(output)
                lineInput, lineOutput = f.readline().strip(), f.readline().strip()
            ioSamples.append((inputs, outputs))
            #print(inputs, "\n\n", outputs, "\n", "--------\n")

    result = []
    for i in range(len(ioSamples)):
        numSuccess, numFailure = 0, 0
        inputs, outputs = ioSamples[i]
        assert len(inputs) == len(outputs), f"lengths of inputs({len(inputs)}) and outputs ({len(outputs)}) must be equal"
        for j in range(len(inputs)):
            scoreToBeMax = model(paramList[i], inputs[j], outputs[j])
            correct = True
            for m in range(len(paramList)):
                if m != i:
                    score = model(paramList[m], inputs[j], outputs[j])
                    if score >= scoreToBeMax:
                        correct = False
                        if debug: print(f"{fileNameList[i]}, i/o {inputs[j]} / {outputs[j]}: model {i}'s score ({scoreToBeMax}) < model {m}'s score ({score})")

            if correct: numSuccess += 1
            else: numFailure += 1
        result.append((numSuccess, numFailure))

    return result

def evaluateModelWithSingleIO(model, paramList, maxIndex, input, output, debug):
    scoreToBeMax = model(paramList[maxIndex], input, output)
    correct = True
    for m in range(len(paramList)):
        if m != maxIndex:
            score = model(paramList[m], input, output)
            if score >= scoreToBeMax:
                correct = False
                if debug: print(f"i/o {input} / {output}: model {maxIndex}'s score ({scoreToBeMax}) < model {m}'s score ({score})")
    return correct


def findAllEven(input):
    return [i for i in input if i % 2 == 0]

def sumAll(input):
    return [sum( i for i in input )]


def model1(param, input, output):
    '''
    Use this learned model and parameters in 'param' 
        to compute score for 'input' and 'output'
    '''
    assert len(input) == NUM_INPUT, f"length of input({len(input)}) must be equal to NUM_INPUTS {NUM_INPUT}"

    # Encode output, such that empty slot, True, and False turn into ENCODE_EMPTY, ENCODE_TRUE, and ENCODE_FALSE
    outputEncoded = []
    for i in output:                    
        if i == "True": outputEncoded.append(ENCODE_TRUE)
        elif i == "False": output.append(ENCODE_FALSE)
        else: outputEncoded.append(i)
    while len(outputEncoded) < NUM_OUTPUT: outputEncoded.append(ENCODE_EMPTY)
    output = outputEncoded

    # Write codes below
    calc = param[0] * output[0] + param[1] * (output[1] + 11)
    
    '''
    합산 프로그램은 output[1]부터 output[4]까지의 값이 무조건 '-100'이 들어가게 된다. 반면 짝수 찾기 프로그램의 경우 output[1]이 '-100'인 경우도 있지만,
    output[1]이 -10 ~ +10 인 경우도 존재한다. 그러므로 output[1]에 '11'을 더하면 짝수 찾기 프로그램에서는 짝수가 두 개 이상인 경우 무조건 양수이지만, 합산 프로그램에서는 항상
    '-90'이므로 무조건 음수이다. 따라서 paramList[0][1]은 '-1'로 paramList[1][1]은 '1'로 설정하여 합산 프로그램은 100% 구분 가능하며 짝수 찾기 프로그램은 짝수가 두 개 이상인 경우 확실하게 구분할 수 있도록 설정하였다.
    '''

    return calc


if __name__ == "__main__":  
    '''
    Test for after-class problems
    '''    
    model = model1
    paramList = [[1, -1], [1, 1]]
    assert len(paramList[0]) == len(paramList[1]), f"the lengths of parameter lists ({len(paramList[0])}, {len(paramList[1])}) must be equal)"

    print()
    print("Correctness test")
    print(" for each case, if your answer does not appear within 1 seconds, consider that you failed the case")
    print()    

    input, output = [5, 2, 2, 2, 2], [13]
    if evaluateModelWithSingleIO(model, paramList, 0, input, output, True): print("P ", end='')
    else: print("F ", end='')      

    input, output = [2, 4, 1, 1, 1], [9]
    if evaluateModelWithSingleIO(model, paramList, 0, input, output, True): print("P ", end='')
    else: print("F ", end='')

    input, output = [5, 2, 2, 2, 2], [2, 2, 2, 2]
    if evaluateModelWithSingleIO(model, paramList, 1, input, output, True): print("P ", end='')
    else: print("F ", end='')

    input, output = [2, 4, 1, 1, 1], [2, 4]
    if evaluateModelWithSingleIO(model, paramList, 1, input, output, True): print("P ", end='')
    else: print("F ", end='')

    print()
    print()

    fileNameList = ["input1-sumAll.txt", "input1-findAllEven.txt"] 
    numSF = evaluateModelWithFiles(model, paramList, fileNameList, True)
    for i in range(len(numSF)):
        print(f"{fileNameList[i]}, # of success/failure: {numSF[i]}, ", end='')
        if numSF[i][0] / sum(numSF[i]) >= 0.75: print("pass")
        else: print("fail")