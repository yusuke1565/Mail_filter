#python kadai7_1.py training.txt
#Ask probability for calculate

import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def detach_Label(line):
    label,sentence = line.split(",",1)
    return label,sentence


def make_word2freq(sentence):  #return word2freq
    w2f={}
    sentence = sentence.rstrip()
    words = mecab.parse(sentence).split(" ")
    for word in words:
        w2f[word] = w2f.get(word,0) +1
    return w2f


def calculate_pLabel(label2f): #calculate probability of label
    label2prob={}
    NofMail=0
    for freq in label2f.values():
        NofMail += freq
    for label in label2f.keys():
        label2prob[label] = float(label2f[label]) / float(NofMail)
    return label2prob


def calculate_pw(label2w2f):  #calculate probability of word
    label2w2cal={}
    wordFreq=0
    for label in label2w2f.keys():
        for word in label2w2f[label].keys():
            wordFreq += label2w2f[label][word]
        for word in label2w2f[label].keys():
            label2w2cal[label] = label2w2cal.get(label,{})
            label2w2cal[label][word] = float(label2w2f[label][word]) / float(wordFreq)
    return label2w2cal


def write_pLabel(label2pLabel):
    with open('pLabel.txt', "w") as f:
        for label in label2pLabel.keys():
            f.write(label + " " + str(label2pLabel[label]) + "\n")


def write_pw(label2w2pw):
    with open('pw_Label.txt', "w") as f:
        for label in label2w2pw.keys():
            for word in label2w2pw[label].keys():
                f.write(label + " " + word + " " + str(label2w2pw[label][word]) + "\n")

def main():
    file = args[1]
    w2f={}
    label2f={}  #label2fleq
    label2w2f={}  #label2word2fleq
    with open(file,'r') as file:
        for line in file:
            label , sentence = detach_Label(line)
            label2f[label] = label2f.get(label,0) +1  #count label
            label2w2f[label] = label2w2f.get(label,{})  #define two dimensions dictionary
            w2f =  make_word2freq(sentence)
            for word in w2f.keys():
                label2w2f[label][word] = label2w2f[label].get(word,0) + w2f[word]

    for label in label2w2f:  #\n is cause of the error
        label2w2f[label].pop("\n")

    label2pLabel = calculate_pLabel(label2f)  #pl=pS,pN,...
    label2w2pw = calculate_pw(label2w2f)  #pw=p(w|S),p(w|N),...

    write_pLabel(label2pLabel)
    write_pw(label2w2pw)


if __name__ == "__main__":
    main()