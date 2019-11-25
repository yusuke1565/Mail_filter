#python kadai7_1.py training.txt
#Ask probability for calculate

def return_label(line):
    l = line.split(",")
    return l[0]


def countWord_perLabel(l,line,l2w2f):  #return fleq word per label
    line = line.rstrip()
    line = mecab.parse(line)
    words = line.split(" ")
    for word in words:
        l2w2f[l][word] = l2w2f[l].get(word, 0) + 1
    return l2w2f


def calculate_pl(l2f,mailLen): #calculate probability of label
    l2cal={}
    for l in l2f.keys():
        l2cal[l] = float(l2f[l]) / float(mailLen)
    return l2cal


def calculate_pw(l2w2f):  #calculate probability of word
    l2w2cal={}
    wordFreq=0
    for l in l2w2f.keys():
        for word in l2w2f[l].keys():
            wordFreq += l2w2f[l][word]
        for word in l2w2f[l].keys():
            l2w2cal[l] = l2w2cal.get(l,{})
            l2w2cal[l][word] = float(l2w2f[l][word]) / float(wordFreq)
    return l2w2cal


def write_pl(l2pl):
    with open('pl.txt', "w") as f:
        for l in l2pl.keys():
            f.write(l + " " + str(l2pl[l]) + "\n")


def write_pw(l2w2pw):
    with open('pw_l.txt', "w") as f:
        for l in l2w2pw.keys():
            for word in l2w2pw[l].keys():
                f.write(l + " " + word + " " + str(l2w2pw[l][word]) + "\n")


import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')

file = args[1]
l2f={}  #label2fleq
l2w2f={}  #label2word2fleq
mailLen=0
with open(file,'r') as file:
    for line in file:
        l = return_label(line)
        l2f[l] = l2f.get(l,0) +1  #count label
        l2w2f[l] = l2w2f.get(l,{})  #define two dimensions dictionary
        l2w2f = countWord_perLabel(l,line,l2w2f)
        mailLen+=1

for l in l2w2f:  #cause of the error
    l2w2f[l].pop("\n")

l2pl = calculate_pl(l2f,mailLen)  #pl=pS,pN,...
l2w2pw = calculate_pw(l2w2f)  #pw=p(w|S),p(w|N),...

write_pl(l2pl)
write_pw(l2w2pw)