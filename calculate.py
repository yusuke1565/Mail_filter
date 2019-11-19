#python kadai7_1.py training.txt
#Ask probability for calculate

import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')

file = args[1]
Swords=[]
Nwords=[]
Sword2fleq={}
Nword2fleq={}
mailLen=0
with open(file,'r') as f:
    for line in f:
        mailLen+=1
        line = line.rstrip()
        text = list(line)
        words = mecab.parse(line).split(' ')
        if text[0] == 'S':
            for word in words:
                Swords.append(word)
                Sword2fleq[word] = Sword2fleq.get(word,0) +1
        elif text[0] =='N':
            for word in words:
                Nwords.append(word)
                Nword2fleq[word] = Nword2fleq.get(word,0) +1

pS = float(Sword2fleq['S']) / float(mailLen)
pN = float(Nword2fleq['N']) / float(mailLen)

Sword2cal={}
Nword2cal={}
SwordLen = len(Swords)
NwordLen = len(Nwords)

for Sword in Sword2fleq.keys():
    Sword2cal[Sword] = float(Sword2fleq[Sword]) / float(SwordLen)

for Nword in Nword2fleq.keys():
    Nword2cal[Nword] = float(Nword2fleq[Nword]) / float(NwordLen)

with open('pSpN.txt',"w") as f:
    f.write(str(pS) + "\n")
    f.write(str(pN) + "\n")

with open('pw_N.txt',"w") as f:
    for Nword in Nword2cal.keys():
        f.write(Nword + " " + str(Nword2cal[Nword]) + "  \n")

with open('pw_S.txt',"w") as f:
    for Sword in Sword2cal.keys():
        f.write(Sword + " " + str(Sword2cal[Sword]) + "  \n")