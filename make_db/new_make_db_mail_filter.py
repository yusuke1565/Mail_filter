import sys
import MeCab
import sqlite3

args = sys.argv
mecab = MeCab.Tagger("-Owakati")


class Mail:
    """
    Mail is label of mail and content.
    """
    def __init__(self, line):
        """
        Go to label and content.
        :param line: 1 line.
        """
        l, c = self.parse(line)
        self.label = l
        self.content = c
        self.words = None

    # ------------------------------------#
    def parse(self, line, delimiter=','):
        """
        Parse mail to label and content.
        :param line: 1 line of mail.
        :param delimiter: Delimiter of label and content.
        :return: Label and content.
        """
        label, content = line.split(delimiter)
        return label, content

    def get_label(self):
        return self.label

    def parse_content(self):
        self.words = mecab.parse(self.get_content()).split(" ")

    def get_content(self):
        return self.content

    def get_words(self):
        if self.words is None:
            self.parse_content()

        return self.words


class Dic_for_freq:
    """
    This class make dictionary for frequency and set data, and output it.
    """
    def __init__(self, list=[]):
        """
        Define dictionary(key2frequency) and go 'set data'.
        :param list(list): Real or char.
        """
        self.k2f = {}
        self.set_data(list)

    # ---------------------------------#
    def set_data(self, list=[]):
        """
        Set data in k2f.
        :param list(list): Real or char.
        """
        for k in list:
            self.k2f[k] = self.k2f.get(k, 0) + 1

    def get_dic(self):
        """
        Return k2f.
        :return: Dictionary for frequency.
        """
        return self.k2f


class Second_dimension_dic_for_freq:
    """
    This class make second dimension dictionary for frequency.
    """
    def __init__(self, category=None, key2freq={}):
        """
        Define dictionary(category2key2frequency) and go 'set data'.
        category2key2frequency is category to key, key to frequency.
        :param category(real or char): category somethings.
                                      Example, label or category.
        :param key2freq(dictionary): Dictionary for frequency.
        """
        self.c2k2f = {}
        self.set_data(category, key2freq)

    # -----------------------------------#
    def set_data(self, c=None, k2f={}):
        """
        Set data in c2k2f.
        :param c(real or char): category something.
        :param k2f(dictionary): Key to frequency.
        """
        if c:
            self.c2k2f[c] = self.c2k2f.get(c, {})
            for k in k2f.keys():
                self.c2k2f[c][k] = self.c2k2f[c].get(k, 0) + k2f[k]

    def get_dic(self):
        """
        Return c2k2f.
        :return: Second dimension dictionary for frequency.
        """
        return self.c2k2f


class Dic_for_prob:
    """
    This class make dictionary for probability.
    """
    def __init__(self, key2freq={}):
        """
        Define dictionary(key2probability) and go 'set data'.
        :param key2freq(dictionary): Key to frequency.
        """
        self.k2p = {}
        self.set_data(key2freq)

    # -------------------------------------#
    def set_data(self, k2f={}):
        """
        Set data in k2p. (probability = frequency / all frequency)
        :param k2f(dictionary): Key to frequency.
        """
        n = 0
        for k in k2f.keys():
            n = n + k2f[k]
        for k in k2f.keys():
            self.k2p[k] = float(k2f[k]) / float(n)

    def get_dic(self):
        """
        Return k2p.
        :return: Dictionary for probability.
        """
        return self.k2p


class Second_dimension_dic_for_prob:
    """
    This class make second dimension dictionary for prob.
    """
    def __init__(self, category2key2freq={}):
        """
        Define dictionary(category2key2probability) and go 'set data'.
        category2key2probability is category to key, key to probability.
        :param category2key2freq(dictionary): category to key. Key to frequency.
        """
        c2k2f = category2key2freq
        self.c2k2p = {}
        self.set_data(c2k2f)

    # ----------------------------------------#
    def set_data(self, c2k2f={}):
        """
        Set data in c2k2p.
        :param c2k2f(dictionary): category to key. Key to frequency.
        """
        for c in c2k2f.keys():
            self.c2k2p[c] = {}
            for k in c2k2f[c].keys():
                self.c2k2p[c][k] = float(c2k2f[c][k]) / float(len(c2k2f[c]))

    def get_dic(self):
        """
        Return c2k2p.
        :return: Second dimension dictionary for prob.
        """
        return self.c2k2p

def filter(category2word2freq={}):
    """
    If word exist over 10 frequency in all category, delete it.
    category2word2freq(dictionary): Second dimension dictionary for freq.
    return (dictionary): Filtered dictionary.
    """
    del2f = {}
    i = 0
    for category in category2word2freq.keys():
        i = i + 1
        for word, freq in category2word2freq[category].items():
            if freq >= 10:
                del2f[word] = del2f.get(word, 0) + 1
    for word, freq in del2f.items():
        if freq >= i:
            for category in category2word2freq.keys():
                 del category2word2freq[category][word]
    return category2word2freq


def main():
    file = args[1]
    labels = []
    i = 0
    with open(file, "r", encoding="utf-8_sig") as f:
        for line in f:
            i = i + 1
            line = line.rstrip()
            mail = Mail(line)  # Mail is instance of class 'Mail'.

            label = mail.get_label()
            labels.append(label)

            words = mail.get_words()
            w2f = Dic_for_freq(words)
            w2f = w2f.get_dic()
            del w2f["\n"]  # '\n' cause error because delete it.

            if i == 1:  # First contact.
                label2w2f = Second_dimension_dic_for_freq(label, w2f)
            else:
                label2w2f.set_data(label, w2f)  # Not first contact.
            del w2f

    label2f = Dic_for_freq(labels)
    label2f = label2f.get_dic()

    label2w2f = label2w2f.get_dic()
    label2w2f = filter(label2w2f)


    label2p = Dic_for_prob(label2f)
    label2p = label2p.get_dic()

    label2w2p = Second_dimension_dic_for_prob(label2w2f)
    label2w2p = label2w2p.get_dic()

    db_name = args[2]
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE word_prob(label text,
                                        word text, prob real)''')
    # word_prob(label| word| probability)
    c.execute('''CREATE TABLE label_prob(label text, prob real)''')
    # label_prob(label| probability)
    for label, w2p in label2w2p.items():
        list1 = [(label, label2p[label])]
        c.executemany("INSERT INTO label_prob VALUES (?,?)", list1)
        for w, prob in w2p.items():
            list2 = [(label, w, prob)]
            c.executemany("INSERT INTO word_prob VALUES (?,?,?)", list2)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
