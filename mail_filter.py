#python kadai7_2.py test.txt
#judge spam mail

import sys
import MeCab
import math
import calculate_probability

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def read_pLabel(read_file = "A"):  #pS,pN,...
    with open(read_file, "r") as f:
        label2pLabel = {}
        for line in f:
            line = line.rstrip()
            labelW = line.split(" ")
            label2pLabel[labelW[0]] = labelW[1]
    return label2pLabel


def read_pw(read_file = "B"):  #p(w|S),p(w|N),...
    with open(read_file,"r") as f:
        label2w2pw={}
        for line in f:
            line = line.rstrip()
            labelWPw = line.split(" ")
            label2w2pw[labelWPw[0]] = label2w2pw.get(labelWPw[0],{}) #define two dimentions dictionary
            label2w2pw[labelWPw[0]][labelWPw[1]] = labelWPw[2]
    return label2w2pw

def count_word(sentence):  #return word2freq
    w2f={}
    sentence = sentence.rstrip()
    words = mecab.parse(sentence).split(" ")
    for word in words:
        w2f[word] = w2f.get(word,0) +1
    return w2f

def calculate_prob(test_w2f, pL, w2pw):  #calculate probability to judge mail
    ans = math.log(float(pL))
    for word in test_w2f.keys():
        ans = ans + math.log( float(w2pw.get(word,0.000000001)) ) * test_w2f[word]
    return ans


def main():
    label2pLabel = read_pLabel(read_file = "pLabel.txt")
    label2w2pw = read_pw(read_file = "pw_Label.txt")

    test_file = args[1]
    NofMail=0
    match=0
    NofJudge_S = 0
    NofTest_label_S = 0
    with open(test_file,"r") as file:
        for line in file:
            NofMail+=1
            test_label , test_mail = calculate_probability.detach_Label(line)
            test_w2f = count_word(test_mail)

            label2p={}
            for label in label2pLabel.keys():
                label2p[label] = calculate_prob(test_w2f, label2pLabel[label], label2w2pw[label])

            a=-99999999
            judge=0

            for label in label2p.keys():
                if a < label2p[label]:
                    a = label2p[label]
                    judge = label

            if test_label == 'S':
                NofTest_label_S+=1

            if judge == 'S':
                NofJudge_S+=1
                if judge == test_label:
                    match+=1

            print(judge)

        print("precision:" + str(match) + "/" + str(NofJudge_S))
        print("recall:" + str(match) + "/" + str(NofTest_label_S))
        if NofJudge_S != 0:
            precision = float(match) / float(NofJudge_S)
            recall = float(match) / float(NofTest_label_S)
            F = (2 * precision * recall) / (precision + recall)
            print("F-measure:" + str(F))


if __name__ == "__main__":
    main()