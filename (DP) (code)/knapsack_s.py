def knapsackS(maxSize, names, sizes, values):
    assert len(names) == len(sizes) and len(sizes) == len(values), f"names({len(names)}, sizes({len(sizes)}, and values({len(values)}) must have the same lengths"
    numItems = len(names)
    memo = [(0, None) for _ in range(maxSize + 1)]
    
    for i in range(1, maxSize + 1):
        for j in range(numItems):
            if sizes[j] <= i and memo[i][0] <= memo[i - sizes[j]][0] + values[j]:
                memo[i] = memo[i - sizes[j]][0] + values[j], j

    result = []
    s = maxSize
    while memo[s][1] != None:
        result.append(names[memo[s][1]])
        s = s - sizes[memo[s][1]]

    return memo[maxSize][0], result
        

if __name__ == "__main__":
    names, sizes, values = ['A'], [5], [10]        
    maxSize = 4
    print(maxSize, knapsackS(maxSize, names, sizes, values))    
    maxSize = 9
    print(maxSize, knapsackS(maxSize, names, sizes, values))

    names, sizes, values = ['A', 'B', 'C', 'D'], [6, 4, 3, 2], [30, 16, 13, 9]        
    for maxSize in range(2, 11):
        print(maxSize, knapsackS(maxSize, names, sizes, values))    
    



    
