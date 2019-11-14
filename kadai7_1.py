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
i=0
with open(file,'r') as f:
    for line in f:
        i+=1
        line = line.rstrip()
        text = list(line)
        words = mecab.parse(line).split(' ')
        if text[0] == 'S':
            for word in words:
                Swords.append(word)
                Sword2fleq[word] = 0
        elif text[0] =='N':
            for word in words:
                Nwords.append(word)
                Nword2fleq[word] = 0

for Sword in Swords:
    Sword2fleq[Sword] += 1
for Nword in Nwords:
    Nword2fleq[Nword] += 1

pS = float(Sword2fleq['S']) / float(i)
pN = float(Nword2fleq['N']) / float(i)

Sword2cal={}
Nword2cal={}
allwordCount = len(Nwords) + len(Swords)
SwordCount = len(Swords)
NwordCount = len(Nwords)
for Sword in Swords:
    Sword2cal[Sword] = float(Sword2fleq[Sword]) / float(SwordCount)
for Nword in Nwords:
    Nword2cal[Nword] = float(Nword2fleq[Nword]) / float(NwordCount)

with open('pSpN.txt',"w") as f:
    f.write("pS=" + str(pS) + "\n")
    f.write("pN=" + str(pN) + "\n")

with open('pw_N.txt',"w") as f:
    for Nword in Nword2fleq.keys():
        f.write("p(%s|N)=" %Nword +str(Nword2cal[Nword]) + "\n")

with open('pw_S.txt',"w") as f:
    for Sword in Sword2fleq.keys():
        f.write("p(%s|S)=" %Sword +str(Sword2cal[Sword]) + "\n")