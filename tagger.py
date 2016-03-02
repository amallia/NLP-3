import string
import re
import csv
import math
def emissionProb(word, pos, emitDict, posDict):
    if word in emitDict :
        if pos in emitDict[word]:
	   pairCount = emitDict[word][pos]
	   totCount = posDict[pos]
	   return float(pairCount)/totCount
        else:
	   return 0
    else:
        return 0

def transProb(pos1, pos2,transDict):
    if pos1 in transDict:

        if pos2 in transDict[pos1]:
	   sumValues = sum(transDict[pos1].values())
	   countpos2 = transDict[pos1][pos2]
	   return float(countpos2)/sumValues
        else:
	   return 0
    else: return 0
def tagger(trainingSet,testSet):
    trainData = open(trainingSet,"r")
    testData = open(testSet,"r")
    res = []
    sent = []
    for line in testData:
        l = line.rstrip()
        if len(l) > 0:
	   sent.append(l)
        else:
	   res.append(' '.join(sent))
	   sent = []
        
    posDict = {} 
    prev = 'S'
    transDict = {}
    emitDict = {}
    posDict[prev] = 0
    for line in trainData:
        sl = line.rstrip().split()
        if len(sl) == 2:

	   if sl[0] in emitDict:
	       if sl[1] not in emitDict[sl[0]]:
		  emitDict[sl[0]][sl[1]] = 1
	       else:
		  emitDict[sl[0]][sl[1]]+= 1
	   else:
	       emitDict[sl[0]] = {}
	       emitDict[sl[0]][sl[1]] = 1
	   if sl[1] not in posDict:
	       posDict[sl[1]] = 1
	   else:
	       posDict[sl[1]]+= 1
	   if prev not in transDict:
	       transDict[prev]={}
	       transDict[prev][sl[1]]=1

	   else:
	       if sl[1] not in transDict[prev]:
		  transDict[prev][sl[1]]=1
	       else:
		  transDict[prev][sl[1]]+=1
	   prev = sl[1]

        else:
	   prev = 'S'
	   posDict[prev]+=1


    output = []
    for sent in res:
        output.append(viterbi(emitDict,transDict,posDict,sent))
    f = open("out",'w')
    writer = csv.writer(f, delimiter = '\t')

    for line in output:
        for o in line:
	   f.write("%s\t%s\n" %(o[0],o[1]))
        f.write("\n")

def viterbi(emitDict,transDict,posDict,sent):
    sentence = sent.split(' ')
    trellis = []
    backtrack = []
    l = len(sentence)
    posList = posDict.keys()
    #posList.append('S')
    for i in xrange(l+1):
        viterbi_scores = dict(zip(posList,[0]*len(posList)))
        viterbi_backtrack = dict(zip(posList,['xyz']*len(posList)))
        if i == 0:
	   viterbi_scores['S'] =  1
	   viterbi_backtrack['S'] = 's'
        trellis.append(viterbi_scores)
        backtrack.append(viterbi_backtrack)
    #print backtrack
    
    #for i in xrange(l+1):
        #print trellis[i]["S"]
    for i in xrange(1,l+1):
        cur = sentence[i-1]
        for to_pos in posList:
	  #max_score = float("-inf")
	  trellis[i][to_pos]= 0
	  for from_pos in  posList:
		 #print from_pos, trellis[i-1][from_pos] 
		 #print cur, from_pos, to_pos, transProb(from_pos,to_pos,transDict), emissionProb(cur,to_pos,emitDict,posDict)
	      score = trellis[i-1][from_pos]*transProb(from_pos,to_pos,transDict)*emissionProb(cur,to_pos,emitDict,posDict)
	      #print score 
	      if trellis[i][to_pos] == 0 or score > trellis[i][to_pos]:
		 max_score  = score
		 trellis[i][to_pos]=score
		 backtrack[i][to_pos]= from_pos
	      
        
        #state = sentence[i]
    best  = '.'
    for s in posList:
        if trellis[l][s] > trellis[l][best]:
	   best = s
    #print "best", best
    out = []
    for i in xrange(l,0,-1):
        out.append((sentence[i-1],best))
        try:
	   best =  backtrack[i][best]
        except KeyError:
	   print backtrack
	   print "keyError",i, sentence[i-1],best
    out.reverse()
    return out


tagger("WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos","WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.words")
