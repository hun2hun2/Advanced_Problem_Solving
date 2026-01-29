import timeit

def binarySearchEQ(numbers, target):
    '''
    Find target in the list numbers
    If the target exists in the list, return its index. Otherwise, return -1
    '''
    def recur(fromIndex, toIndex):
        if fromIndex > toIndex: return -1

        mid = int((fromIndex + toIndex) / 2)        
        if numbers[mid] < target: return recur(mid + 1, toIndex)
        elif numbers[mid] > target: return recur(fromIndex, mid - 1)
        else: return mid

    return recur(0, len(numbers) - 1) 

def binarySearchMaxLessThan(numbers, target):
    
    def recur(fromIndex, toIndex, best_index=-1):
        if fromIndex > toIndex: return best_index  # 가장 가까운 값 반환

        mid = (fromIndex + toIndex) // 2
        if numbers[mid] < target:
            return recur(mid + 1, toIndex, mid)  # 후보 갱신 후 오른쪽 탐색
        else:
            return recur(fromIndex, mid - 1, best_index)  # 왼쪽 탐색

    return recur(0, len(numbers) - 1)

def binarySearchMinGreaterThan(numbers, target):
    
    def recur(fromIndex, toIndex, best_index = -1):
        if fromIndex > toIndex:
            return best_index  # 가장 적절한 후보 반환

        mid = (fromIndex + toIndex) // 2
        if numbers[mid] > target:
            return recur(fromIndex, mid - 1, mid)  # 후보 갱신 후 왼쪽 탐색
        else:
            return recur(mid + 1, toIndex, best_index)  # 오른쪽 탐색

    return recur(0, len(numbers) - 1)

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

def findLongestConsecutivePrimeSum(*sums):  
    maxSum = max(sums)
    sqrtMax = int(maxSum ** 0.5) + 1
    prime = [True] * (maxSum + 1)
    prime[0] = prime[1] = False
    p = 2    
    while p*p <= maxSum:
        if prime[p]:
            prime[p*p::p] = [False] * ((maxSum - p*p) // p + 1)            
        p += 1    

    psResult = [i for i in range(len(prime)) if prime[i]]
    lastIndex = [0] * (maxSum + 1)
    sumArr = [[0] * (sqrtMax * 2) for _ in range((sqrtMax * 2))]
    sumArr[0][0] = 2
    for i in range(1, sqrtMax * 2):
        sumArr[0][i] = sumArr[0][i-1] + psResult[i]
        if sumArr[0][i] > maxSum * 2:
            lastIndex[0] = i
            break

    resultList = []
    for sum in sums:
        validLength = 0        
        lb = 0
        rb = binarySearchMaxLessThan(sumArr[0][0:lastIndex[0]], sum)
        row = 0
        lbLength = 0
        length = 0
        resultSum = 0

        while row < sqrtMax * 2 and lb < rb:
            sumChange = 0
            for i in range(rb, lb, -1):
                if sumArr[row][i] > sum:
                    break
                if prime[sumArr[row][i]] == True:
                    resultSum = sumArr[row][i]
                    lbLength = i + 1
                    length = i + 1 - row
                    sumChange = 1
                    break

            row += 1
            validChecker = 0
            
            if row > 0:
                if sumArr[row][row] == 0:
                    for j in range(row, sqrtMax*2):
                        sumArr[row][j] = sumArr[0][j] - sumArr[0][row - 1]
                        if sumArr[row][j] > sum and validChecker == 0:
                            validLength = j
                            rb = binarySearchMaxLessThan(sumArr[row][row:validLength], sum) + row
                            validChecker = 1
                        
                        if sumArr[row][j] > maxSum:
                            lastIndex[row] = j
                            break
                        
                else:
                    rb = binarySearchMaxLessThan(sumArr[row][row:lastIndex[row]], sum) + row
            
            if sumChange == 1:
                lb = lbLength
            else:
                lb += 1
                
        resultList.append((resultSum, length))

    return resultList


def speedCompare1(*sums):
    '''
    Compute the entire 2D table in advance
    This function is used to evaluate the execution time of findLongestConsecutivePrimeSum()
    '''
    maxSum = max(sums)
    
    prime = [True] * maxSum
    prime[0] = prime[1] = False
    p = 2    
    while p*p <= maxSum:
        if prime[p]:
            for i in range(p*p, maxSum, p): prime[i] = False
        p += 1
    
    primeSumFirstRow = []
    sum = 0    
    for p in range(maxSum):
        if prime[p]: 
            sum += p
            primeSumFirstRow.append(sum)

    primeSums = [primeSumFirstRow]
    for row in range(1, len(primeSumFirstRow)):
        primeSumCurrentRow = []
        for i in range(len(primeSumFirstRow)):
            if i < row: primeSumCurrentRow.append(None)
            else: primeSumCurrentRow.append(primeSumFirstRow[i] - primeSumFirstRow[row - 1])
        primeSums.append(primeSumCurrentRow)
        

def speedCompare2(*sums):
    '''
    Perform prime sieve for each N in sums
    This function is used to evaluate the execution time of findLongestConsecutivePrimeSum()
    '''
    for sum in sums:
        prime = [True] * sum
        prime[0] = prime[1] = False
        p = 2    
        while p*p <= sum:
            if prime[p]:
                for i in range(p*p, sum, p): prime[i] = False
            p += 1
        
        primeSumFirstRow = []
        sum = 0    
        for p in range(sum):
            if prime[p]: 
                sum += p
                primeSumFirstRow.append(sum)      


if __name__ == "__main__":
    print("Correctness test for findLongestConsecutivePrimeSum()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    correct = True

    if findLongestConsecutivePrimeSum(100, 200, 300) == [(41, 6), (197, 12), (281, 14)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if findLongestConsecutivePrimeSum(500, 600, 700, 800, 900, 1000) == [(499, 17), (499, 17), (499, 17), (499, 17), (857, 19), (953, 21)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False
        
    if findLongestConsecutivePrimeSum(2000, 5000, 10000, 20000, 50000) == [(1583, 27), (4651, 45), (9521, 65), (16823, 81), (49279, 137)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if findLongestConsecutivePrimeSum(60000, 70000, 80000, 90000, 100000) == [(55837, 146), (66463, 158), (78139, 167), (86453, 178), (92951, 183)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if findLongestConsecutivePrimeSum(1000000, 5000000, 8000000) == [(997651, 543), (4975457, 1150), (7998491, 1433)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if findLongestConsecutivePrimeSum(10000000) == [(9951191, 1587)]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    print()
    print()
    print("Speed test for findLongestConsecutivePrimeSum()")
    if not correct: print("fail (since the algorithm is not correct)")
    else:
        repeat = 10
        sums = [5000]
        tSpeedCompare1 = timeit.timeit(lambda: speedCompare1(*sums), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: findLongestConsecutivePrimeSum(*sums), number=repeat)/repeat    
        print(f"For input sums: {sums}")
        print(f"Average running times of the submitted code and the code that computes the entire 2D table in advance: {tSubmittedCode:.10f} and {tSpeedCompare1:.10f}")    
        if tSubmittedCode < tSpeedCompare1: print("pass")
        else: print("fail")
        print()

        sums = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000]
        tSpeedCompare2 = timeit.timeit(lambda: speedCompare2(*sums), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: findLongestConsecutivePrimeSum(*sums), number=repeat)/repeat    
        print(f"For input sums: {sums}")
        print(f"Average running times of the submitted code and the code that performs sieve for each sum in sums: {tSubmittedCode:.10f} and {tSpeedCompare2:.10f}")
        if tSubmittedCode < tSpeedCompare2: print("pass")
        else: print("fail")
    

    

