#python kadai6.py training.txt
#Count word in training.txt

import MeCab
import sys

args=sys.argv
mecab=MeCab.Tagger("-Owakati")

file=args[1]
with open(file,"r") as f:
    text = f.read()
    words = mecab.parse(text).split(' ')

fleq = len(words)

print "word count:",fleq