# -*- coding: utf-8 -*-
import sys
from gensim.models import word2vec

model = word2vec.Word2Vec.load_word2vec_format('aozora_model', binary=True)

def get_most_similar(word, n):
  try:
    result = model.most_similar(positive = word, negative = [], topn = n)
  except:
    return []
  return list(i[0] for i in result)

if __name__ == "__main__":
  word = sys.argv[1]
  for i in get_most_similar(word.decode("utf-8"), 5):
    print i
