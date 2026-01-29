import timeit


def handshake(n):
    '''
    Return the number of ways to pair 2n vertices around a circle, such that the lines connecting pairs do not cross one another
    Input:
        n -- number of vertices
    '''
    assert type(n) == int, "n = {n} must be an integer"
    assert n >= 0 and n <= 100, f"n = {n} must be >=0 and <=100"

    '''
    Write your codes below
    '''

    shakeNum = [0 for _ in range(n + 1)]
    shakeNum[0] = 1
    for i in range(1, n + 1):
        for j in range(0, i):
            shakeNum[i] = shakeNum[i] + shakeNum[j] * shakeNum[i - j - 1]

    return shakeNum[n]


def kanpsackSW(maxSize, maxWeight, names, sizes, weights, values):
    '''
    Given a knapsack with maxSize and maxWeight,
    return a 2-tuple, (the max sum of values that fit the knapsack, the corresponding list of items)
    Input:
        maxSize -- size of the knapsack
        maxWeight -- maximum weight of items that the knapsack can carry
        names, sizes, weights, values -- list of item names, sizes, weights, and values
            for example, ['A', 'B'], [1, 2], [5, 4], [10, 7] indicates two items,
                (i) 'A' with size 1, weight 5, and value 10
                (ii) 'B' with size 2, weight 4, and value 7        
    '''
    assert len(names) == len(sizes) and len(sizes) == len(weights) and len(weights) == len(values), f"names({len(names)}, sizes({len(sizes)}, weights({len(weights)}), and values({len(values)}) must have equal lengths"

    '''
    Write your codes below
    '''

    numItems = len(sizes)
    memo = [[(0, None) for _ in range(maxWeight + 1)] for _ in range(maxSize + 1)]
    for i in range(maxSize + 1):
        for j in range(maxWeight + 1):
            for s in range(numItems):
                if sizes[s] <= i and weights[s] <= j and memo[i][j][0] <= memo[i-sizes[s]][j-weights[s]][0] + values[s]:
                    memo[i][j] = memo[i-sizes[s]][j-weights[s]][0] + values[s], s
    
    result = []
    p = maxSize
    q = maxWeight
    while memo[p][q][1] != None:
        nowItem = memo[p][q][1]
        result.append(names[memo[p][q][1]])
        p = p - sizes[nowItem]
        q = q - weights[nowItem]

    return memo[maxSize][maxWeight][0], result


def speedCompare1(n):
    memo = [0] * (n + 1)
    memo[0:2] = [2, 2]
    for i in range(2, n + 1):
        for j in range(1, i): memo[i] += 2 * memo[j] + memo[j-1]
    return memo[n]


def speedCompare2(maxSize, maxWeight, names, sizes, weights, values):
    numItems = len(names)
    memo = [[(0, [0 for _ in range(numItems)]) for _ in range(maxWeight + 1)] for _ in range(maxSize + 1)]
    
    for i in range(1, maxSize + 1):
        for j in range(1, maxWeight + 1):
            for k in range(numItems):
                if sizes[k] <= i and weights[k] <= j:
                    item1 = memo[i - sizes[k]][j - weights[k]][0] + values[k]
                    item2 = [item for item in memo[i - sizes[k]][j - weights[k]][1]]                    
                    item2[k] += 1
                    memo[i][j] = item1, item2

    return memo[maxSize][maxWeight]


if __name__ == "__main__":

    print("Correctness test for handshake()")
    correct = True

    if handshake(0) == 1: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if handshake(1) == 1: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(2) == 2: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if handshake(3) == 5: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(4) == 14: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(5) == 42: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if handshake(6) == 132: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(7) == 429: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if handshake(8) == 1430: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(15) == 9694845: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if handshake(99) == 227508830794229349661819540395688853956041682601541047340: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    if handshake(100) == 896519947090131496687170070074100632420837521538745909320: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    print()
    print()
    print("Speed test for handshake()")
    print("    if the test runs for more than 1 second, then you fail,")
    print("    so stop the test and consider using 'memoization' correctly in your code")
    if not correct: print("fail (since the algorithm is not correct)")
    else:        
        n = 100
        tHandshake = timeit.timeit(lambda: handshake(100), number=n)/n
        tSpeedCompare1 = timeit.timeit(lambda: speedCompare1(100), number=n)/n       
        print(f"Average running time for handshake ({tHandshake:.10f}) and speedCompare1*5 ({tSpeedCompare1*5:.10f})")        
        if tHandshake < tSpeedCompare1 * 5: print("pass")
        else: print("fail")
    print()


    print("Correctness test for knapsackSW()")
    correct = True

    sizes = [3, 2, 1, 4, 1]
    weights = [2, 1, 3, 2, 1]
    values = [12, 10, 20, 15, 5]
    names = ['A', 'B', 'C', 'D', 'E']    
    
    if kanpsackSW(1, 1, names, sizes, weights, values) == (5, ['E']): print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if kanpsackSW(1, 3, names, sizes, weights, values) == (20, ['C']): print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    if kanpsackSW(2, 1, names, sizes, weights, values) == (10, ['B']): print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    v, r = kanpsackSW(5, 5, names, sizes, weights, values)
    if v == 40: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    v, r = kanpsackSW(8, 10, names, sizes, weights, values)
    if v == 70: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False

    v, r = kanpsackSW(10, 6, names, sizes, weights, values)
    if v == 50: print("P ", end='') 
    else: 
        print("F ", end='')
        correct = False
    
    print()
    print()
    print("Speed test for knapsackSW()")
    print("    if the test runs for more than 1 second, then you fail,")
    print("    so stop the test and consider using 'memoization' correctly in your code")
    if not correct: print("fail (since the algorithm is not correct)")
    else:        
        sizes = [3, 2, 1, 4, 1, 1, 1, 2, 4, 3, 2, 1, 2, 5]
        weights = [2, 1, 3, 2, 1, 4, 2, 1, 3, 3, 5, 7, 2, 2]
        values = [12, 10, 20, 15, 5, 7, 8, 2, 4, 9, 1, 25, 27, 3]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']        
        n = 30
        tKnapsack = timeit.timeit(lambda: kanpsackSW(40, 40, names, sizes, weights, values), number=n)/n        
        tSpeedCompare2 = timeit.timeit(lambda: speedCompare2(40, 40, names, sizes, weights, values), number=n)/n
        print(f"Average running time for knapsack ({tKnapsack:.10f} and speedCompare2/1.5 ({tSpeedCompare2/1.5:.10f}))")                
        if tKnapsack * 1.5 < tSpeedCompare2: print("pass")
        else: print("fail")
    print()