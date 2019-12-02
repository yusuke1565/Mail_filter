#python kadai7_1.py training.txt
#Ask probability for calculate

import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def detach_Label(line):
    L,sentence = line.split(",")
    return L[0],sentence


def make_word2freq(sentence):  #return word2freq
    w2f={}
    sentence = sentence.rstrip()
    words = mecab.parse(sentence).split(" ")
    for word in words:
        w2f[word] = w2f.get(word,0) +1
    return w2f


def calculate_pL(L2f): #calculate probability of label
    L2prob={}
    mailLen=0
    for freq in L2f.values():
        mailLen += freq
    for L in L2f.keys():
        L2prob[L] = float(L2f[L]) / float(mailLen)
    return L2prob


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

def main():
    file = args[1]
    w2f={}
    L2f={}  #label2fleq
    L2w2f={}  #label2word2fleq
    with open(file,'r') as file:
        for line in file:
            L , sentence = detach_Label(line)
            L2f[L] = L2f.get(L,0) +1  #count label
            L2w2f[L] = L2w2f.get(L,{})  #define two dimensions dictionary
            w2f =  make_word2freq(sentence)
            for word in w2f.keys():
                L2w2f[L][word] = L2w2f[L].get(word,0) + w2f[word]

    for L in L2w2f:  #\n is cause of the error
        L2w2f[L].pop("\n")

    L2pL = calculate_pL(L2f)  #pl=pS,pN,...
    L2w2pw = calculate_pw(L2w2f)  #pw=p(w|S),p(w|N),...

    write_pL(L2pL)
    write_pw(L2w2pw)


if __name__ == "__main__":
    main()