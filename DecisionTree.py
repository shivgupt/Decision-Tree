import math
import sys

def getConditionalEntropy(Y,X,dataset):        # Y: Class Label, X: Feature
    total = len(dataset)
    X_value = sorted(set(i[X] for i in dataset))  # all distinct values of given feature in the set
    temp_x_y = {}
    temp_x = {}
    Hyx = 0.000000
    for y in Y_value:                               #Create keys for all combination of y,x
        for x in X_value:
            temp_x_y[y+x] = []

    for r in dataset:                               #catogorize the data where Y=y and X=x
        temp_x_y[r[Y]+r[X]].append(r)

    for x in X_value:                               #store no.of instances with X=x
        temp_x[x] = sum(len(temp_x_y[y+x]) for y in Y_value)
    for y in Y_value:
        for x in X_value:
            pxy = len(temp_x_y[y+x])
            if pxy != 0:
                Hyx += (pxy/(total+0.0))*(math.log((temp_x[x]/(pxy+0.0))))
    return Hyx

def getDecisionTree(dataset,feature,depth,classLabel):
    Hyx = [getConditionalEntropy(classLabel,i,dataset) for i in feature]
    best = feature.pop(Hyx.index(min(Hyx)))
    decisionTree =  [best]
    decisionTree.insert(1,splitTree(dataset,feature,depth-1,best))
    finalizeClass(decisionTree, depth)
    return decisionTree

def splitTree(Set,feature,depth,best):
    subtree = {}
    for record in Set:
        k = record[best]
        if k in subtree:
            subtree[k].append(record)
        else:
            subtree[k] = [record]
    if len(subtree) == 1:
        return Set
    elif len(feature) <= 0 or depth == 0:
        return subtree
    else:
        result = {}
        for subset in subtree:
            if len(sorted(set(i[classLabel] for i in subtree[subset]))) > 1:
                Hyx = [getConditionalEntropy(classLabel, i, subtree[subset]) for i in feature]
                best = feature[(Hyx.index(min(Hyx)))]
                node = [best]
                attribute  = list(feature)
                attribute.remove(best)
                result[subset] = node
                node.insert(1,splitTree(subtree[subset],attribute,depth-1,best))
            else:
                result[subset] = subtree[subset]
        return result

def finalizeClass(root,d):
    if type(root) is list:
        if type(root[0]) is not list:
            root[1] = finalizeClass(root[1], d - 1)
        else:
            label = {}
            for i in root:
                if i[classLabel] in label:
                    label[i[classLabel]]+=1
                else:
                    label[i[classLabel]] = 1
            k = label.keys()
            v = label.values()
            root = k[v.index(max(v))]
            return root
    else:
        for i in root:
            root[i] = finalizeClass(root[i],d)
    return root

def getDataset(fileName):                #return list where each item is a list representing one example
    return [line.split(',',) for line in [line.rstrip('\r\n') for line in open(fileName,"r") ]]

def getClass(record,tree,feature):
    if type(tree) is list:
        return getClass(record,tree[1],record[feature])
    else:
        if feature in tree:
            for i in tree:
                if i == feature:
                    if type(tree[i]) is list:
                        return getClass(record,tree[i],tree[i][0])
                    else:
                        return tree[i]
        else:
            inter = {}
            for i in tree:
                if type(tree[i]) is list:
                    cl = getClass(record,tree[i],tree[i][0])
                else:
                    cl = tree[i]
                if cl in inter:
                    inter[cl]+=1
                else:
                    inter[cl] =1
            k = inter.keys()
            v = inter.values()
            return k[v.index(max(v))]
def printConfusionMatrix(fp,fn,tp,tn):
    print "******** Confusion Matrix for depth = ",depth,"********"
    print " tn = ",tn," fn = ",fn
    print " fn = ", tn, " tp = ", tp
    return
def test(testset,classLabel,tree):
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    for i in testset:
        cl = getClass(i,tree,tree[0])
        if cl == i[classLabel]:
            if cl == Y_value[1]:
                tp+=1
            else:
                tn+=1
        elif cl == Y_value[1]:
            fp+=1
        else:
            fn+=1
    printConfusionMatrix(tp,tn,fp,fn)
    global Accuracy
    Accuracy= (tp+tn)/(TestTotal+0.0)
    return

if len(sys.argv) != 5:
    print "Missing or Improper input !!"
    print "DecisionTree.py <training set file> <testset file> <column# of classLabel> <column# of UniqueID>"
    exit(0)
classLabel = int(sys.argv[3])
uniqueId = int(sys.argv[4])
dataset = getDataset(sys.argv[1])
testset = getDataset(sys.argv[2])
TestTotal = len(testset)
Accuracy = 0
features = []
Y_value = sorted(set(i[classLabel] for i in dataset))  # all distinct values of class label in the set
for i in range(0,len(dataset[0])):
    if i != classLabel and i != uniqueId:
        features.append(i)
copy = list(features)
for depth in range(1,17):
    tree = getDecisionTree(dataset,features,depth,classLabel)
    test(testset, classLabel, tree)
    features = list(copy)