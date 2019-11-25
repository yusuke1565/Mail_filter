#python kadai7_1.py training.txt
#Ask probability for calculate

def return_Label(line):
    L = line.split(",")
    return L[0]


def countWord_perLabel(L,line,L2w2f):  #return fleq word per label
    line = line.rstrip()
    line = mecab.parse(line)
    words = line.split(" ")
    for word in words:
        L2w2f[L][word] = L2w2f[L].get(word, 0) + 1
    return L2w2f


def calculate_pL(L2f,mailLen): #calculate probability of label
    L2cal={}
    for L in L2f.keys():
        L2cal[L] = float(L2f[L]) / float(mailLen)
    return L2cal


def calculate_pw(L2w2f):  #calculate probability of word
    L2w2cal={}
    wordFreq=0
    for L in L2w2f.keys():
        for word in L2w2f[L].keys():
            wordFreq += L2w2f[L][word]
        for word in L2w2f[L].keys():
            L2w2cal[L] = L2w2cal.get(L,{})
            L2w2cal[L][word] = float(L2w2f[L][word]) / float(wordFreq)
    return L2w2cal


def write_pL(L2pL):
    with open('pL.txt', "w") as f:
        for L in L2pL.keys():
            f.write(L + " " + str(L2pL[L]) + "\n")


def write_pw(L2w2pw):
    with open('pw_L.txt', "w") as f:
        for L in L2w2pw.keys():
            for word in L2w2pw[L].keys():
                f.write(L + " " + word + " " + str(L2w2pw[L][word]) + "\n")


import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')

file = args[1]
L2f={}  #label2fleq
L2w2f={}  #label2word2fleq
mailLen=0
with open(file,'r') as file:
    for line in file:
        L = return_Label(line)
        L2f[L] = L2f.get(L,0) +1  #count label
        L2w2f[L] = L2w2f.get(L,{})  #define two dimensions dictionary
        L2w2f = countWord_perLabel(L,line,L2w2f)
        mailLen+=1

for L in L2w2f:  #cause of the error
    L2w2f[L].pop("\n")

L2pL = calculate_pL(L2f,mailLen)  #pl=pS,pN,...
L2w2pw = calculate_pw(L2w2f)  #pw=p(w|S),p(w|N),...

write_pL(L2pL)
write_pw(L2w2pw)