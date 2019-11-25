#python kadai6.py training.txt
#Count word in training.txt

def wordCount(line):
    freq=0
    line=line.rstrip()
    line=mecab.parse(line)
    words=line.split(" ")
    freq+=len(words)
    return freq

def showFreq(freq):
    print(freq)


import MeCab
import sys
args=sys.argv
mecab=MeCab.Tagger("-Owakati")

file=args[1]
freq=0
with open(file,"r") as f:
    for line in f:
        a+=1
        freq+=wordCount(line)

showFreq(freq)