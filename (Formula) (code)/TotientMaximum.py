import math
import timeit
from pathlib import Path

def gcd3(a, b):
    while b != 0:
        if a > b: a, b = b, a % b
        else: b = b % a
    return a

def phiUsingGCD(n):
    phi = 0
    for i in range(1, n):
        if gcd3(i, n) == 1: phi += 1
    return phi

def totientMaximum1(N):
    nOverPhiMax = 0
    nMax = 0
    for n in range(2, N + 1):
        phi = phiUsingGCD(n)
        nOverPhi = n / phi
        if nOverPhiMax < nOverPhi:
            nOverPhiMax = nOverPhi
            nMax = n
    return nOverPhiMax, nMax

def phiUsingPrimeFactorization(n):
    phi = n
    
    if n % 2 == 0: # Check to see if 2 is a prime factor
        phi = phi * (2 - 1) / 2        
        while n % 2 == 0: n /= 2

    p = 3 # Check to see if odd numbers in 3 ~ sqrt(n) are prime factors
    while p*p <= n:
        if n % p == 0:
            phi = phi * (p - 1) / p
            while n % p == 0: n /= p
        p += 2
    
    if n > 2: phi = phi * (n - 1) / n # What is left in n must also be a prime factor if n > 2

    return phi

def totientMaximum2(N):
    nOverPhiMax = 0
    nMax = 0
    for n in range(2, N + 1):
        phi = phiUsingPrimeFactorization(n)
        nOverPhi = n / phi
        if nOverPhiMax < nOverPhi:
            nOverPhiMax = nOverPhi
            nMax = n
    return nOverPhiMax, nMax

def findPrimes(maxN):
    '''
    Find all primes <= maxN and return them in a list
    '''
    prime = [True] * (maxN + 1)
    prime[0] = prime[1] = False
    p = 2    
    while p*p <= maxN:
        if prime[p]:
            prime[p*p::p] = [False] * ((maxN - p*p) // p + 1)            
        p += 1

    return [i for i in range(len(prime)) if prime[i]]

def totientMaximum3(*Ns):
    maxN = max(Ns)
    limit = min(1000, maxN)
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    p = 2    
    while p*p <= limit:
        if prime[p]:
            prime[p*p::p] = [False] * ((limit - p*p) // p + 1)            
        p += 1

    result = [i for i in range(len(prime)) if prime[i]]
    totientList = []
    totientList.append(2)
    resultList = []

    for number in Ns:
        if totientList[len(totientList)-1] > number:
            for i in range(len(totientList)):
                if totientList[i] <= number:
                    answer = totientList[i]
                else:
                    break
        else:
            bp = 0
            while bp == 0:
                j = len(totientList)
                totientList.append(totientList[j-1] * result[j])
                if totientList[j] > number:
                    answer = totientList[j-1]
                    bp = 1
                else:
                    j += 1
        resultList.append(answer)

    return resultList    


def totientMinimum(*Ns): 
    maxN = max(Ns)
    prime = [True] * (maxN + 1)
    prime[0] = prime[1] = False
    p = 2    
    while p*p <= maxN:
        if prime[p]:
            prime[p*p::p] = [False] * ((maxN - p*p) // p + 1)            
        p += 1

    resultList = []

    for number in Ns:
        for i in range(number, 1, -1):
            if prime[i] == True:
                resultList.append(i)
                break

    return resultList


def readFileIntoIntegerList(fileName):
    '''
    Read integers in filename into a list and return the list
    This function is used for evaluation
    '''
    filePath = Path(__file__).with_name(fileName)   # Use the location of the current .py file
    result = []
    with filePath.open('r') as f:        
        line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
        while line:                                
            if len(line) > 0 and line.isnumeric(): result.append(int(line))
            line = f.readline().strip()
    return result


if __name__ == "__main__":
    # Test for in-class problems
    # functions = [totientMaximum1]
    # for f in functions:
    #     for i in range(2, 12):
    #         print(i, f(i), end=' ')
    #     print()

    #     n, repeat = 100, 10
    #     tTotientMaximum = timeit.timeit(lambda: f(n), number=repeat)/repeat    
    #     print(f"{f.__name__}({n}) took {tTotientMaximum} seconds on average")

    # Test for after-class problems
    print()
    print("Correctness test for totientMaximum3()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    if totientMaximum3(2, 3, 4, 5, 6, 7, 8, 9, 10, 11) == [2, 2, 2, 2, 6, 6, 6, 6, 6, 6]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMaximum3(50, 500, 1000000) == [30, 210, 510510]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMaximum3(10000000, 1000000000) == [9699690, 223092870]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMaximum3(10000000000, 1000000000000, 10000000000000) == [6469693230, 200560490130, 7420738134810]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMaximum3(1000000000000000, 10000000000000000, 100000000000000000) == [304250263527210, 304250263527210, 13082761331670030]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    inputLines = readFileIntoIntegerList("testInput1.txt")
    outputLines = readFileIntoIntegerList("testOutput1.txt")
    if totientMaximum3(*inputLines) == outputLines: print("P ", end='')
    else:
        print("F ", end='')
        correct = False
    print(timeit.timeit(lambda: totientMaximum3(*inputLines), number=1))
    
    
    print()
    print("Correctness test for totientMinimum()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    if totientMinimum(2, 3, 4, 5, 6, 7, 8, 9, 10, 11) == [2, 3, 3, 5, 5, 7, 7, 7, 7, 11]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMinimum(50, 500, 1000) == [47, 499, 997]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMinimum(5000, 10000, 50000) == [4999, 9973, 49999]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if totientMinimum(100000, 500000, 1000000) == [99991, 499979, 999983]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    inputLines = readFileIntoIntegerList("testInput2.txt")
    outputLines = readFileIntoIntegerList("testOutput2.txt")
    if totientMinimum(*inputLines) == outputLines: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    print(timeit.timeit(lambda: totientMinimum(*inputLines), number=1))
