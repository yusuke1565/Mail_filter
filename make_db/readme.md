# 教師データベースについて

ここでは、教師データベースについて記す。


### 教師データベースの作成

教師データベースの作成には、trainigデータとしてラベル付きメール本文を63個、そしてmake_db_mail_filter.pyを使用した。


### 文法

'''bash
$python make_db_mail_filter.py <-.txt>
'''

'<-.txt>'は、人手で集めたトレーニングデータ。


### デモ

'''bash
$python make_db_mail_filter.py training.txt
'''

すると、[training_mail_filter.db](https://github.com/yusuke1565/mail_filter/database)が作成される。


### トレーニングデータ

トレーニングデータには、<ラベル>,<メール本文>である。下記が例である。

![training](./image/tarining.png)


