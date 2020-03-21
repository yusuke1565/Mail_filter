# Categorize mail.

import sys
import MeCab
import math
import sqlite3
from make_db import make_db_mail_filter

args = sys.argv
mecab = MeCab.Tagger('-Owakati')


def load_db(db="training.db"):
    """
    Load database and make label2word2freq and label2prob.
    :param db(database): Training data.
    :return label2w2p(dictionary): Label to word to probability.
            label2p(dictionary): Label to probability.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    label2w2p = {}
    for row1 in c.execute('SELECT * FROM word_prob'):
        # Set data label2w2p
        label, word, prob = row1[0], row1[1], row1[2]
        label2w2p[label] = label2w2p.get(label, {})
        label2w2p[label][word] = prob

    label2p = {}
    for row2 in c.execute('SELECT * FROM label_prob'):
        # Set data label2p
        label, prob = row2[0], row2[1]
        label2p[label] = prob
    c.close()
    return label2w2p, label2p


def count_word(content):
    """
    Count word in content and make word2freq.
    :param content(char): Words and numbers.
    :return w2f(dictionary): Word to frequency.
    """
    content = content.rstrip()
    words = mecab.parse(content).split(" ")
    w2f = make_db_mail_filter.Dic_for_freq(words)
    w2f = w2f.get_dic()
    return w2f


def calculate_prob(test_w2f={}, label_prob=0, word2prob={}):
    """
    Calculate probability to categorize mail
    :param test_w2f(dictionary): Word to frequency in test data.
    :param label_prob(real): Probability for label.
    :param word2prob(dictionary): Word to probability in training data.
    :return p(char): Answer calculation.
    """
    p = math.log(float(label_prob))
    for word, f in test_w2f.items():
        p = p + math.log(float(word2prob.get(word, 0.000000001))) * f
    return p


def main(db, content):
    """
    Filterize mail.
    :param db(database): Training data.
    :param content(char): Words and numbers.
    :return judge(char): Answer catego
    """
    label2w2p, label2p = load_db(db)

    test_w2f = count_word(content)
    a = -99999999
    for label, p in label2p.items():
        ans_p = calculate_prob(test_w2f, label_prob=p,
                                     word2prob=label2w2p[label])

        if a < ans_p:
            a = ans_p
            judge = label

    return judge


if __name__ == "__main__":
    main()
