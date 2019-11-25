#python kadai7_2.py test.txt
#judge spam mail

def make_L2pL(file):  #pS,pN
    with open(file, "r") as f:
        L2pL = {}
        for line in f:
            line = line.rstrip()
            LW = line.split(" ")
            L2pL[LW[0]] = LW[1]
    return L2pL


def make_L2w2pw(file):  #p(w|S),p(w|N),...
    with open(file,"r") as f:
        L2w2pw={}
        for line in f:
            line = line.rstrip()
            LWPw = line.split(" ")
            L2w2pw[LWPw[0]] = L2w2pw.get(LWPw[0],{}) #define two dimentions dictionary
            L2w2pw[LWPw[0]][LWPw[1]] = LWPw[2]
    return L2w2pw


def countWord(line):  #return word2freq
    w2f={}
    line = line.rstrip()
    line = mecab.parse(line)
    words = line.split(" ")
    for word in words:
        w2f[word] = w2f.get(word,0) +1
    return w2f


def calculate_p(w2f, pL, w2pw):  #calculate probability to judge mail
    ans = math.log(float(pL))
    for word in w2f.keys():
        ans = ans + math.log( float(w2pw.get(word,0.000000000000001)) ) * w2f[word]
    return ans



import sys
import MeCab
import math

args = sys.argv
mecab = MeCab.Tagger('-Owakati')
file = args[1]

L2pL = make_L2pL("pL.txt")
L2w2pw = make_L2w2pw("pw_L.txt")


with open(file,"r") as file:
    for line in file:
        w2f = {}
        w2f = countWord(line)

        L2p={}
        for L in L2pL.keys():
            L2p[L] = calculate_p(w2f, L2pL[L], L2w2pw[L])

        a=-9999999999999
        judge=0
        for L in L2p.keys():
            if a < L2p[L]:
                a = L2p[L]
                judge = L

        print(judge)