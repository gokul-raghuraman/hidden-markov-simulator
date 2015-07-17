"""
This program calculates the best path
and its corresponding probability for a model (with 2 states)
for the sequence D# D C# C C# D D# D C# C
"""

pathProbDictAvalanche = {}

class AvalancheA:
    def __init__(self, p, id, pathParent=None):
        self.nextA = None
        self.nextB = None
        self.prob = p
        self.id = id
        self.costA = 0.6
        self.costB = 0.4
        self.type = 'A'
        self.pathParent = pathParent
        
        
class AvalancheB:
    def __init__(self, p, id, pathParent=None):
        self.nextA = None
        self.nextB = None
        self.prob = p
        self.id = id
        self.costA = 0.4
        self.costB = 0.5
        self.type = 'B'
        self.pathParent = pathParent


def recurseAvalanche(node, probSoFar, exitProb):
    if node.nextA is None and node.nextB is None:
        prob = probSoFar * node.prob * exitProb
        pathProbDictAvalanche[buildPathAvalanche(node, '')] = prob
    if node.nextA is not None:
        node.nextA.pathParent = node
        recurseAvalanche(node.nextA, probSoFar * node.prob * node.costA, exitProb)
    if node.nextB is not None:
        node.nextB.pathParent = node
        recurseAvalanche(node.nextB, probSoFar * node.prob * node.costB, exitProb)

def calculatePathsAvalanche(rootNode, entryProb, exitProb):
    recurseAvalanche(rootNode, entryProb, exitProb)
   
def buildPathAvalanche(node, curPath):
    if node.pathParent is None:
        return '%s%s -> %s' % (node.type, node.id, curPath)
    if curPath == '':
        return buildPathAvalanche(node.pathParent, '%s%s' % (node.type, node.id))
    else:
        return buildPathAvalanche(node.pathParent, '%s%s -> %s' % (node.type, node.id, curPath))   
    
def backTrack(node):
    if node.pathParent is None:
        print("Node : " + str(node.type) + str(node.id))
        return
    backTrack(node.pathParent)
    print("Node : " + str(node.type) + str(node.id))
                

if __name__ == '__main__':
    nodeAProbs = [0.4, 0.4, 0.1, 0.1, 0.1, 0.4, 0.4, 0.4, 0.1, None]
    nodeBProbs = [None, 0.1, 0.4, 0.4, 0.4, 0.1, 0.1, 0.1, 0.4, 0.4]
    nodeListA = []
    nodeListB = []
    for i in range(10):
        nodeListA.append(AvalancheA(nodeAProbs[i], i))
        nodeListB.append(AvalancheB(nodeBProbs[i], i))
        
    for i in range(len(nodeListA)):
        if i < 8:
            nodeListA[i].nextA = nodeListA[i + 1]
        if i < 9:
            nodeListA[i].nextB = nodeListB[i + 1]
        
        if i > 0 and i < 8:
            nodeListB[i].nextA = nodeListA[i + 1]
        if i > 0 and i < 9:
            nodeListB[i].nextB = nodeListB[i + 1]
    
    calculatePathsAvalanche(nodeListA[0], 0.5, 0.1)

    print("Number of paths = " + str(len(pathProbDictAvalanche.keys())))
    
    bestPath = ''
    maxProb = 0
    for path in pathProbDictAvalanche:
        #print("PATH = " + str(path))
        #print("PROBABILITY = " + str(pathProbDict[path]))
        if pathProbDictAvalanche[path] > maxProb:
            maxProb = pathProbDictAvalanche[path]
            bestPath = path
            
    print('\n')    
    print("\nBest path = " + bestPath)
    print("Best path probability = " + str(maxProb))
        
        