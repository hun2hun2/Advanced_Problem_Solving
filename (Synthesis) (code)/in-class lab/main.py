import argparse
import IOsample # IOSample.py processes input-1
import command  # command.py processes input-2
from pathlib import Path

if __name__ == '__main__':
    # create an instance of argument parser
    parser = argparse.ArgumentParser(description='-e filename -c filename')

    parser.add_argument('-e', help='input file that includes i/o samples', default='input1-findalleven.txt')
    parser.add_argument('-c', help='input file that describes usable commands', default='input2-command.txt')

    args = parser.parse_args()
    #print(args)
    
    ios = IOsample.read_file(Path(__file__).with_name(args.e))	# parse io samples
    #ios.toString()   

    expressions = command.read_file(Path(__file__).with_name(args.c))     # parse expressions

    '''
    for i in expressions:
        print(str(i)+':')
        print(expressions[i].toString())
        print()
    '''
    
    tree = command.deepcopyExpression(expressions['e0'], 0, 20) # make tree
    #print(tree.toString())
 
    command.initializeCodeGenerationSequence()
    code = command.generateNextDistinctCode(tree)
    while code != None:        
        result = IOsample.validateCode(ios, code)
        if result[0] > 0 and result[1] == 0:
            print("---- code #", command.distinctCodeCount, "----") 
            print(code)
            print()
        code = command.generateNextDistinctCode(tree)        
        
    print("A total of", command.distinctCodeCount, "distinct codes explored")

