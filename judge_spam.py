#python kadai7_2.py test.txt
#judge spam mail

import sys
import MeCab
import math
import calculate_probability

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def make_Label2pLabel(file):  #pS,pN,...
    with open(file, "r") as f:
        label2pLabel = {}
        for line in f:
            line = line.rstrip()
            labelW = line.split(" ")
            label2pLabel[labelW[0]] = labelW[1]
    return label2pLabel


def make_Label2word2pw(file):  #p(w|S),p(w|N),...
    with open(file,"r") as f:
        label2w2pw={}
        for line in f:
            line = line.rstrip()
            labelWPw = line.split(" ")
            label2w2pw[labelWPw[0]] = label2w2pw.get(labelWPw[0],{}) #define two dimentions dictionary
            label2w2pw[labelWPw[0]][labelWPw[1]] = labelWPw[2]
    return label2w2pw


def calculate_prob(test_w2f, pL, w2pw):  #calculate probability to judge mail
    ans = math.log(float(pL))
    for word in test_w2f.keys():
        ans = ans + math.log( float(w2pw.get(word,0.000000001)) ) * test_w2f[word]
    return ans


def main():
    file = args[1]

    label2pLabel = make_Label2pLabel("pLabel.txt")
    label2w2pw = make_Label2word2pw("pw_Label.txt")


    NofMail=0
    match=0
    NofJudge_S = 0
    NofTest_Label_S = 0
    with open(file,"r") as file:
        for line in file:
            NofMail+=1
            test_Label , test_sentence = calculate_probability.detach_Label(line)
            test_w2f = calculate_probability.make_word2freq(test_sentence)

            label2p={}
            for label in label2pLabel.keys():
                label2p[label] = calculate_prob(test_w2f, label2pLabel[label], label2w2pw[label])

            a=-99999999
            judge=0

            for label in label2p.keys():
                if a < label2p[label]:
                    a = label2p[label]
                    judge = label

            if test_Label == 'S':
                NofTest_Label_S+=1

            if judge == 'S':
                NofJudge_S+=1
                if judge == test_Label:
                    match+=1

            print(judge)

        print("precision:" + str(match) + "/" + str(NofJudge_S))
        print("recall:" + str(match) + "/" + str(NofTest_Label_S))
        precision = float(match) / float(NofJudge_S)
        recall = float(match) / float(NofTest_Label_S)
        F = (2 * precision * recall) / (precision + recall)
        print("F-measure:" + str(F))


if __name__ == "__main__":
    main()