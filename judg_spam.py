#python kadai7_2.py test.txt
#judge spam mail

def make_l2pl(file):  #pS,pN
    with open(file, "r") as f:
        l2pl = {}
        for line in f:
            line = line.rstrip()
            LW = line.split(" ")
            l2pl[LW[0]] = LW[1]
    return l2pl


def make_l2w2pw(file):  #p(w|S),p(w|N),...
    with open(file,"r") as f:
        l2w2pw={}
        for line in f:
            line = line.rstrip()
            LWPw = line.split(" ")
            l2w2pw[LWPw[0]] = l2w2pw.get(LWPw[0],{}) #define two dimentions dictionary
            l2w2pw[LWPw[0]][LWPw[1]] = LWPw[2]
    return l2w2pw


def countWord(line):  #return word2freq
    w2f={}
    line = line.rstrip()
    line = mecab.parse(line)
    words = line.split(" ")
    for word in words:
        w2f[word] = w2f.get(word,0) +1
    return w2f


def calculate_p(w2f, pl, w2pw):  #calculate probability to judge mail
    ans = math.log(float(pl))
    for word in w2f.keys():
        ans = ans + math.log( float(w2pw.get(word,0.000000000000001)) ) * w2f[word]
    return ans



import sys
import MeCab
import math

args = sys.argv
mecab = MeCab.Tagger('-Owakati')
file = args[1]

l2pl = make_l2pl("pl.txt")
l2w2pw = make_l2w2pw("pw_l.txt")


with open(file,"r") as file:
    for line in file:
        w2f = {}
        w2f = countWord(line)

        l2p={}
        for l in l2pl.keys():
            l2p[l] = calculate_p(w2f, l2pl[l], l2w2pw[l])

        a=-9999999999999
        judge=0
        for l in l2p.keys():
            if a < l2p[l]:
                a = l2p[l]
                judge = l

        print(judge)