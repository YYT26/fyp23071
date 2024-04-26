# -*- coding: utf-8 -*-

from polyglot.downloader import downloader
from polyglot.mapping import Embedding
from polyglot.text import Text
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

import numpy as np


import pandas as pd

downloader.download("embeddings2.zh")
embeddings = Embedding.load("/Users/leeszechoi/polyglot_data/embeddings2/zh/embeddings_pkl.tar.bz2")

# print(type(sum([embeddings["hello"],embeddings["world"]])))
# print(embeddings["hello"].shape)
# print(sum([embeddings["hello"],embeddings["world"]]).shape)

df = pd.read_csv("~/Downloads/data (1).csv",names=["ori_id","link","title","date","content","emoji","label","PIC"])

df["combined"] = df["title"] + df["content"]

# df["Tokens"] = df["combined"].apply(lambda x: jieba.lcut(x))

# print(df["Tokens"].values[0:5])


df["label"] = (df["label"]=="Yes")
e = []
for x in df["combined"].values:
    text=Text(x, hint_language_code="zh")
    em = sum([embeddings[y] for y in text.words if y in embeddings])
    if isinstance(em,int):
        e.append([0]*64)
    else:
        e.append(sum([embeddings[y] for y in text.words if y in embeddings]))

X = np.array(e)

y = np.array(df["label"].values)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
svm = SVC(gamma='auto')

svm.fit(X_train,y_train)

y_predict = svm.predict(X_test)
print(accuracy_score(y_test,y_predict))

print(confusion_matrix(y_test,y_predict))


