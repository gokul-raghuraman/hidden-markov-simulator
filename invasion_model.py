"""
This program calculates the best path
and its corresponding probability for the model (with 3 states)
for the sequence D# D C# C C# D D# D C# C
"""

pathProbDictInvasion = {}

class InvasionA:
    def __init__(self, p, id, pathParent=None):
        self.nextA = None
        self.nextB = None
        self.prob = p
        self.id = id
        self.costA = 0.6
        self.costB = 0.4
        self.type = 'A'
        self.pathParent = pathParent
        
        
class InvasionB:
    def __init__(self, p, id, pathParent=None):
        self.nextB = None
        self.nextC = None
        self.prob = p
        self.id = id
        self.costB = 0.7
        self.costC = 0.3
        self.type = 'B'
        self.pathParent = pathParent
        
class InvasionC:
    def __init__(self, p, id, pathParent=None):
        self.nextC = None
        self.prob = p
        self.id = id
        self.costC = 0.6
        self.type = 'C'
        self.pathParent = pathParent

def buildPath(node, curPath):
    if node.pathParent is None:
        return '%s%s -> %s' % (node.type, node.id, curPath)
    if curPath == '':
        return buildPath(node.pathParent, '%s%s' % (node.type, node.id))
    else:
        return buildPath(node.pathParent, '%s%s -> %s' % (node.type, node.id, curPath))   
    

def recurse(node, probSoFar):
    if node.type == 'C':
        if node.nextC is None:
            prob = probSoFar * node.prob * 0.4
            pathProbDictInvasion[buildPath(node, '')] = prob
    if node.type == 'A':
        if node.nextA is not None:
            node.nextA.pathParent = node
            recurse(node.nextA, probSoFar * node.prob * node.costA)
        if node.nextB is not None:
            node.nextB.pathParent = node
            recurse(node.nextB, probSoFar * node.prob * node.costB)
    elif node.type == 'B':
        if node.nextB is not None:
            node.nextB.pathParent = node
            recurse(node.nextB, probSoFar * node.prob * node.costB)
        if node.nextC is not None:
            node.nextC.pathParent = node
            recurse(node.nextC, probSoFar * node.prob * node.costC)
    elif node.type == 'C':
        if node.nextC is not None:
            node.nextC.pathParent = node
            recurse(node.nextC, probSoFar * node.prob * node.costC)
            
      
if __name__ == '__main__':
    nodeAProbs = [0.6, 0.2, 0.1, 0.1, 0.1, 0.2, 0.6, 0.2, None, None]
    nodeBProbs = [None, 0.7, 0.1, 0.1, 0.1, 0.7, 0.1, 0.7, 0.1, None]
    nodeCProbs = [None, None, 0.2, 0.6, 0.2, 0.1, 0.1, 0.1, 0.2, 0.6]
    nodeListA = []
    nodeListB = []
    nodeListC = []
    
    for i in range(10):
        nodeListA.append(InvasionA(nodeAProbs[i], i))
        nodeListB.append(InvasionB(nodeBProbs[i], i))
        nodeListC.append(InvasionC(nodeCProbs[i], i))
    
    
    for i in range(len(nodeListA)):
        if i < 7:
            nodeListA[i].nextA = nodeListA[i + 1]
        if i < 8:
            nodeListA[i].nextB = nodeListB[i + 1]
        
        if i > 0 and i < 8:
            nodeListB[i].nextB = nodeListB[i + 1]
        if i > 0 and i < 9:
            nodeListB[i].nextC = nodeListC[i + 1]
            
        if i > 1 and i < 9:
            nodeListC[i].nextC = nodeListC[i + 1]
    
    
    recurse(nodeListA[0], 0.5)
    
    print("Number of paths = " + str(len(pathProbDictInvasion.keys())))
    
    
    bestPath = ''
    maxProb = 0
    for path in pathProbDictInvasion:
        #print("PATH = " + str(path))
        #print("PROBABILITY = " + str(pathProbDict[path]))
        if pathProbDictInvasion[path] > maxProb:
            maxProb = pathProbDictInvasion[path]
            bestPath = path
               
    print("\nBest path = " + bestPath)
    print("Best path probability = " + str(maxProb))
    
    