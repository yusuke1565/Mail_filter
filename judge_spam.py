#python kadai7_2.py test.txt
#judge spam mail

import sys
import MeCab
import math
import calculate_probability

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def make_Label2pL(file):  #pS,pN,...
    with open(file, "r") as f:
        L2pL = {}
        for line in f:
            line = line.rstrip()
            LW = line.split(" ")
            L2pL[LW[0]] = LW[1]
    return L2pL


def make_Label2word2pw(file):  #p(w|S),p(w|N),...
    with open(file,"r") as f:
        L2w2pw={}
        for line in f:
            line = line.rstrip()
            LWPw = line.split(" ")
            L2w2pw[LWPw[0]] = L2w2pw.get(LWPw[0],{}) #define two dimentions dictionary
            L2w2pw[LWPw[0]][LWPw[1]] = LWPw[2]
    return L2w2pw


def calculate_prob(test_w2f, pL, w2pw):  #calculate probability to judge mail
    ans = math.log(float(pL))
    for word in test_w2f.keys():
        ans = ans + math.log( float(w2pw.get(word,0.000000001)) ) * test_w2f[word]
    return ans


def main():
    file = args[1]

    L2pL = make_Label2pL("pL.txt")
    L2w2pw = make_Label2word2pw("pw_L.txt")


    mailLen=0
    match=0
    with open(file,"r") as file:
        for line in file:
            mailLen+=1
            test_L , test_sentence = calculate_probability.detach_Label(line)
            test_w2f = calculate_probability.make_word2freq(test_sentence)

            L2p={}
            for L in L2pL.keys():
                L2p[L] = calculate_prob(test_w2f, L2pL[L], L2w2pw[L])

            a=-99999999
            judge=0
            for L in L2p.keys():
                if a < L2p[L]:
                    a = L2p[L]
                    judge = L

            if judge == test_L:
                match+=1

            print(judge)

        print("precision:" + str(match) + "/" + str(mailLen))



if __name__ == "__main__":
    main()