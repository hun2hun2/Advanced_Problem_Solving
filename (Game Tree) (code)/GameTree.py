import math
import random
import timeit
from queue import Queue
#from pathlib import Path
from abc import ABC, abstractmethod


class Player(ABC): # extends ABC(Abstract Base Class) to become an abstract class
    '''
    Abstract parent class of all player classes 
        that declares methods that must be implemented
    '''
    @abstractmethod
    def __init__(self, numBlack, numWhite, player): pass

    @abstractmethod
    def doMyTurn(self): pass
    # return (c, n), meaning that we move n(> 1) coins of color c(0 or 1)

    @abstractmethod
    def doOthersTurn(self, color, number): pass


class PTreePlayer(Player):
    def __init__(self, numBlack, numWhite, player): 
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.maxNumSimulations = 50
        self.CONST_C = math.sqrt(2)
        self.expandTree()
    
    def expandTree(self):
        while self.root[2][0] + self.root[2][1] < self.maxNumSimulations:
            node = self.root
            while True:
                if node[1][0] == 0 and node[1][1] == 0: return
                if node[1][0] > 0 and node[3][0] == None:
                    maxChild = (1 - node[0], [node[1][0] - 1, node[1][1]], [0, 0], [None, None, None, None], node)
                    node[3][0] = maxChild
                    break
                elif node[1][0] > 1 and node[3][1] == None:
                    maxChild = (1 - node[0], [node[1][0] - 2, node[1][1]], [0, 0], [None, None, None, None], node)
                    node[3][1] = maxChild
                    break
                elif node[1][1] > 0 and node[3][2] == None:
                    maxChild = (1 - node[0], [node[1][0], node[1][1] - 1], [0, 0], [None, None, None, None], node)
                    node[3][2] = maxChild
                    break
                elif node[1][1] > 1 and node[3][3] == None:
                    maxChild = (1 - node[0], [node[1][0], node[1][1] - 2], [0, 0], [None, None, None, None], node)
                    node[3][3] = maxChild
                    break
                else:
                    node1 = node[3][0]
                    node2 = node[3][1]
                    node3 = node[3][2]
                    node4 = node[3][3]
                    nodeList = [node1, node2, node3, node4]
                    node1Score = -1
                    node2Score = -1
                    node3Score = -1
                    node4Score = -1
                    sp = node[2][0] + node[2][1]
                    if node[0] == 0:
                        if node1 != None:
                            node1Score = node1[2][0] / (node1[2][0] + node1[2][1]) + self.CONST_C * math.sqrt(math.log(sp) / (node1[2][0] + node1[2][1]))
                        if node2 != None:
                            node2Score = node2[2][0] / (node2[2][0] + node2[2][1]) + self.CONST_C * math.sqrt(math.log(sp) / (node2[2][0] + node2[2][1]))
                        if node3 != None:
                            node3Score = node3[2][0] / (node3[2][0] + node3[2][1]) + self.CONST_C * math.sqrt(math.log(sp) / (node3[2][0] + node3[2][1]))
                        if node4 != None:
                            node4Score = node4[2][0] / (node4[2][0] + node4[2][1]) + self.CONST_C * math.sqrt(math.log(sp) / (node4[2][0] + node4[2][1]))
                    elif node[0] == 1:
                        if node1 != None:
                            node1Score = 1 - (node1[2][0] / (node1[2][0] + node1[2][1])) + self.CONST_C * math.sqrt(math.log(sp) / (node1[2][0] + node1[2][1]))
                        if node2 != None:
                            node2Score = 1 - (node2[2][0] / (node2[2][0] + node2[2][1])) + self.CONST_C * math.sqrt(math.log(sp) / (node2[2][0] + node2[2][1]))
                        if node3 != None:    
                            node3Score = 1 - (node3[2][0] / (node3[2][0] + node3[2][1])) + self.CONST_C * math.sqrt(math.log(sp) / (node3[2][0] + node3[2][1]))
                        if node4 != None:
                            node4Score = 1 - (node4[2][0] / (node4[2][0] + node4[2][1])) + self.CONST_C * math.sqrt(math.log(sp) / (node4[2][0] + node4[2][1]))
                    maxScore = node1Score
                    scoreList = [node1Score, node2Score, node3Score, node4Score]
                    maxNode = 0
                    for i in range(1, 4):
                        if maxScore < scoreList[i]:
                            maxScore = scoreList[i]
                            maxNode = i
                    node = nodeList[maxNode]

            coinList = [maxChild[1][0], maxChild[1][1]]
            playerSide = maxChild[0]
            win = False
            while True:
                blackMax = 0
                whiteMax = 0
                coinSide = 0
                if coinList[0] == 0 and coinList[1] == 0:
                    if playerSide == 0:
                        win = True
                    elif playerSide == 1:
                        win = False
                    break
                if coinList[0] > 1:
                    blackMax = 2
                elif coinList[0] == 1:
                    blackMax = 1
                elif coinList[0] == 0:
                    blackMax = 0
                if coinList[1] > 1:
                    whiteMax = 2
                elif coinList[1] == 1:
                    whiteMax = 1
                elif coinList[1] == 0:
                    whiteMax = 0
                if blackMax == 0:
                    randInt = random.randint(1, whiteMax)
                    coinSide = 1
                elif whiteMax == 0:
                    randInt = random.randint(1, blackMax)
                    coinSide = 0
                else:
                    coinSide = random.randint(0, 1)
                    if coinSide == 0:
                        randInt = random.randint(1, blackMax)
                    elif coinSide == 1:
                        randInt = random.randint(1, whiteMax)
                coinList[coinSide] -= randInt
                playerSide = 1 - playerSide
            
            if win == True:
                nodeToRoot = maxChild
                while nodeToRoot[4] != None:
                    nodeToRoot[2][0] += 1
                    nodeToRoot = nodeToRoot[4]
                nodeToRoot[2][0] += 1
            else:
                nodeToRoot = maxChild
                while nodeToRoot[4] != None:
                    nodeToRoot[2][1] += 1
                    nodeToRoot = nodeToRoot[4]
                nodeToRoot[2][1] += 1

    def doMyTurn(self): 
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        maxWinRate, childWithMaxWinRate = None, None
        for child in self.root[3]:
            if child != None:
                if maxWinRate == None: maxWinRate, childWithMaxWinRate = child[2][self.player]/sum(child[2]), child
                else:
                    winRate = child[2][self.player]/sum(child[2])
                    if winRate > maxWinRate: maxWinRate, childWithMaxWinRate = winRate, child
        
        if maxWinRate == None: assert False, f"expandTree(self) is not properly implemented"

        if self.root[1][0] > childWithMaxWinRate[1][0]: color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else: color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]

        self.root = childWithMaxWinRate
        self.expandTree()

        return color, number

    def doOthersTurn(self, color, number): 
        # move to a child node
        # (color, number) = (0, 1), (0, 2), (1, 1), (1, 2) map to the child with index 0, 1, 2, and 3, respectively
        self.root = self.root[3][color * 2 + number - 1]
        self.expandTree()

    def __str__(self): # called when this instance is printed - return nodes' info in BFS order
        result = [f"A total of {sum(self.root[2]) + 1} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            if node[0] != currentPlayerInPreviousNode: result.append("") # break a line if depth increases
            result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player]/sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")            
            for child in node[3]:
                if child != None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)
    
    def countNodes(self):        
        q = Queue()
        q.put(self.root)
        count = 0
        while not q.empty():
            node = q.get()
            count += 1
            for child in node[3]:
                if child != None: q.put(child)
        return count


class TreePlayer(Player):    
    def __init__(self, numBlack, numWhite, player):
        def addChild(childIndex, numBlackMinus, numWhiteMinus):
            nonlocal node, q
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            child = ((node[0] + 1) % 2, [node[1][0] - numBlackMinus, node[1][1] - numWhiteMinus], [0, 0], [None, None, None, None], node)
            node[3][childIndex] = child
            q.put(child)
            self.numNodes += 1
        
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.numNodes = 1
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node[1][0] == 0 and node[1][1] == 0: # end of game
                parent = node
                while parent != None:
                    parent[2][node[0]] += 1     # add numWins
                    parent = parent[4]          # move up to the parent
            else:                
                if node[1][0] >= 1: addChild(0, 1, 0) # add a child with one fewer black coin
                if node[1][0] >= 2: addChild(1, 2, 0) # add a child with two fewer black coins
                if node[1][1] >= 1: addChild(2, 0, 1) # add a child with one fewer white coin
                if node[1][1] >= 2: addChild(3, 0, 2) # add a child with two fewer white coins
                    
    def __str__(self): # called when this instance is printed - return nodes' info in BFS order
        result = [f"A total of {self.numNodes} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            if node[0] != currentPlayerInPreviousNode: result.append("") # break a line if depth increases
            result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player]/sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")            
            for child in node[3]:
                if child != None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)

    def doMyTurn(self):
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        maxWinRate, childWithMaxWinRate = None, None
        for child in self.root[3]:
            if child != None:
                if maxWinRate == None: maxWinRate, childWithMaxWinRate = child[2][self.player]/sum(child[2]), child
                else:
                    winRate = child[2][self.player]/sum(child[2])
                    if winRate > maxWinRate: maxWinRate, childWithMaxWinRate = winRate, child
        if self.root[1][0] > childWithMaxWinRate[1][0]: color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else: color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]
        self.root = childWithMaxWinRate
        return color, number

    def doOthersTurn(self, color, number):
        # move to a child node
        # (color, number) = (0, 1), (0, 2), (1, 1), (1, 2) map to the child with index 0, 1, 2, and 3, respectively
        self.root = self.root[3][color * 2 + number - 1] 


class RandomPlayer(Player):
    def __init__(self, numBlack, numWhite, player):
        self.numCoins = [numBlack, numWhite]

    def doMyTurn(self):
        if self.numCoins[0] >= 1 and self.numCoins[1] >= 1: color = random.randint(0,1)
        elif self.numCoins[0] >= 1: color = 0
        else: color = 1

        number = random.randint(1, min(self.numCoins[color], 2))
        self.numCoins[color] -= number

        return color, number
    
    def doOthersTurn(self, color, number):
        self.numCoins[color] -= number


def runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, debug):
    '''
    Run black-white coin game and return the winner
        numBlack, numWhite: number of black and white coins
        PlayerClass0, PlayerClass1: two players' classes. Player 0 does the first turn.
        debug: if true, print each step of the game
    '''
    assert issubclass(PlayerClass0, Player), f"PlayerClass0({PlayerClass0.__name__}) must be a subclass of Player"
    assert issubclass(PlayerClass1, Player), f"PlayerClass1({PlayerClass1.__name__}) must be a subclass of Player"

    players = [PlayerClass0(numBlack, numWhite, 0), PlayerClass1(numBlack, numWhite, 1)]
    numCoins = [numBlack, numWhite]    
    currentPlayer, otherPlayer = 0, 1
    while numCoins[0] > 0 or numCoins[1] > 0:        
        color, number = players[currentPlayer].doMyTurn()
        players[otherPlayer].doOthersTurn(color, number)

        if debug: print(f"player {currentPlayer}: ({numCoins[0]}, {numCoins[1]}) --> ", end='')
        numCoins[color] -= number
        if debug: print(f"({numCoins[0]}, {numCoins[1]})")

        currentPlayer, otherPlayer = otherPlayer, currentPlayer

    if debug: print(f"player {currentPlayer} wins")
    return currentPlayer # taking the last coin loses the game


if __name__ == "__main__":    
    '''
    Test for in-class problems
    '''
    # Create and print a sample tree
    # TreePlayer(# of black coins, # of white coins, 0(1st player) or 1(2nd player))
    #print(TreePlayer(2, 1, 1))    

    # Run one sample game with output into stdin
    # runBWGame(# of black coins, # of white coins, 1st player's class, 2nd player's class, True(output into stdin) or False(no output))
    #print(runBWGame(2, 1, RandomPlayer, TreePlayer, True)) # Run one sample game with output into stdin

    # Run multiple games and collect statistics on winning rates and running times
    '''numBlack, numWhite = 3, 3
    PlayerClass0, PlayerClass1 = TreePlayer, RandomPlayer
    numGames = 10
    numWins = [0, 0]    
    for i in range(numGames):
        numWins[runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False)] += 1
    print(f"out of {numGames} games, player 0 and 1 win ({numWins[0]}, {numWins[1]}) times")
    
    tGame = timeit.timeit(lambda: runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False), number=numGames)/numGames
    print(f"Average running time is {tGame:.10f} for inputs ({numBlack}, {numWhite}, {PlayerClass0.__name__}, {PlayerClass1.__name__})")'''

    # Test for after-class problems
    print()
    print("Correctness test for PTreePlayer")
    print(" if your answer does not appear within 5 seconds, consider that you failed the case")
    correct = True
    
    # Case 1: PTreePlayer(1, 1, 0) must build the same tree all the time, as shown below
    #
    # A total of 5 nodes
    # (1,1), win rate 1.00 (4/4)
    #
    # (0,1), win rate 1.00 (2/2)
    # (1,0), win rate 1.00 (2/2)
    #
    # (0,0), win rate 1.00 (1/1)
    # (0,0), win rate 1.00 (1/1)
    #
    ws11 = True
    for i in range(10):        
        t = PTreePlayer(1, 1, 0)
        child1, child2 = t.root[3][0], t.root[3][2]  # two children of the root
        if t.countNodes() == 5 and\
        t.root[0] == 0 and t.root[1] == [1, 1] and t.root[2] == [4, 0] and t.root[4] is None and\
        all(t.root[3][i] is not None for i in [0, 2]) and all(t.root[3][i] is None for i in [1, 3]) and\
        child1[0] == 1 and child1[1] == [0, 1] and child1[2] == [2, 0] and (child1[3][2] is not None and all(child1[3][i] is None for i in [0, 1, 3])) and child1[4] == t.root and\
        child2[0] == 1 and child2[1] == [1, 0] and child2[2] == [2, 0] and (child2[3][0] is not None and all(child2[3][i] is None for i in [1, 2, 3])) and child2[4] == t.root:
            gchild1, gchild2 = child1[3][2], child2[3][0]  # two grand children of the root
            if gchild1[0] == 0 and gchild1[1] == [0, 0] and gchild1[2] == [1, 0] and all(gchild1[3][i] is None for i in [0, 1, 2, 3]) and gchild1[4] == child1 and\
            gchild2[0] == 0 and gchild2[1] == [0, 0] and gchild2[2] == [1, 0] and all(gchild2[3][i] is None for i in [0, 1, 2, 3]) and gchild2[4] == child2: pass
            else: ws11 = False
        else: ws11 = False                   
    if ws11: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False
    
    #
    # root 아래 3개의 자식 [1,1], [0,1], [2,0]을 추가하는데
    #       이 중 자식 [2,0]을 추가한 후 simulation한 결과가 선공의 패배라면
    #       자식 [0,1] 아래에 하나의 자식 [0,0]을 추가한 후 더는 노드를 추가하지 않고 종료하게 됨
    #       이 때 root에는 선공 승리 2, 후공 승리 2가 기록되어 있음
    #
    ws21 = False
    for i in range(10):                        
        t = PTreePlayer(2, 1, 0)
        if t.root[2] == [2, 2]: ws21 = True        
    if ws21: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False
    
    #
    # root 아래 3개의 자식 [1,1], [0,1], [2,0] 중
    #      자식 [1,1]은 선공의 승률이 항상 0이므로
    #      [1,1] 아래에는 더는 새로운 자식이 추가되지 않음
    #
    ws21 = True
    for i in range(10):                        
        t = PTreePlayer(2, 1, 1)
        if t.root[3][0] is None or not all(t.root[3][0][3][i] is None for i in [0, 1, 2, 3]): ws21 = False
    if ws21: print("P ", end='\n')
    else: 
        print("F(check to see if you correctly applied min-max) ", end='\n')
        correct = False

    t = PTreePlayer(100, 100, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    t = PTreePlayer(1000, 1000, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='\n')
    else: 
        print("F ", end='\n')
        correct = False

    numWins = [0, 0]
    for i in range(10):             
        numWins[runBWGame(3, 3, PTreePlayer, RandomPlayer, False)] += 1
    if numWins == [10, 0]: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(5, 5, PTreePlayer, RandomPlayer, False)] += 1
    if numWins[0] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(0, 30, RandomPlayer, PTreePlayer, False)] += 1
    if numWins[1] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(20, 20, RandomPlayer, PTreePlayer, False)] += 1    
    if numWins[1] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    print()
    print()
    print("Speed test for expandTree()")    
    if not correct: print("fail (since the algorithm is not correct)")
    else:        
        numCoins, repeat = 4, 20
        tSpeedCompare1 = timeit.timeit(lambda: runBWGame(numCoins, numCoins, TreePlayer, RandomPlayer, False), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: runBWGame(numCoins, numCoins, PTreePlayer, RandomPlayer, False), number=repeat)/repeat
        print(f"For {numCoins} coins")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and TreePlayer/3 {tSpeedCompare1/3:.10f}")        
        if tSubmittedCode * 3 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()
        
