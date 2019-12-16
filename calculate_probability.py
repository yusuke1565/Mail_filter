#python kadai7_1.py training.txt
#Ask probability for calculate

import MeCab
import sys

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def detach_label(line):
    label, mail = line.split(",",1)
    return label, mail


def count_label(label, label2freq):
    label2freq[label] = label2freq.get(label, 0) + 1
    return label2freq


def count_by_label(label, mail, label2w2f):
    w2f = {}
    words = mecab.parse(mail).split(" ")
    for word in words:
        w2f[word] = w2f.get(word, 0) + 1
    for word in w2f.keys():
        label2w2f[label][word] = label2w2f[label].get(word, 0) + w2f[word]
    return label2w2f

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


def write_pLabel(label2pLabel, write_file = 'A'):
    with open(write_file, "w") as f:
        for label in label2pLabel.keys():
            f.write(label + " " + str(label2pLabel[label]) + "\n")


def write_pw(label2w2pw, write_file = 'B'):
    with open(write_file, "w") as f:
        for label in label2w2pw.keys():
            for word in label2w2pw[label].keys():
                f.write(label + " " + word + " " + str(label2w2pw[label][word]) + "\n")

def main():
    file = args[1]
    label2f={}  #label2fleq
    label2w2f={}  #label2word2fleq
    with open(file,'r') as file:
        for line in file:
            line = line.rstrip()
            label , mail = detach_label(line)
            label2f = count_label(label, label2f)
            label2w2f[label] = label2w2f.get(label, {})  #define two dimensions dictionary
            label2w2f = count_by_label(label, mail, label2w2f)

    for label in label2w2f:  #\n is cause of the error
        label2w2f[label].pop("\n")

    label2pLabel = calculate_pLabel(label2f)  #pl=pS,pN,...
    label2w2pw = calculate_pw(label2w2f)  #pw=p(w|S),p(w|N),...

    write_pLabel(label2pLabel, write_file = 'pLabel.txt')
    write_pw(label2w2pw, write_file = 'pw_label.txt')


if __name__ == "__main__":
    main()