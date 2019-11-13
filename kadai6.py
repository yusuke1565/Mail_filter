#python kadai6.py training.txt
#Count word in training.txt

# -*- coding: utf-8 -*-
import MeCab
import sys
args=sys.argv
mecab=MeCab.Tagger("-Owakati")
file=args[1]

with open(file,"r") as f:
    a=f.read()
    words=mecab.parse(a).split(' ')

count=len(words)

print "word count:",count