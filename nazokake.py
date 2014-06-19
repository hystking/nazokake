# -*- coding: utf-8 -*-
import urllib, urllib2, json
from xml.etree.ElementTree import *
import aozora_sim
import xml

f_apikey = open("apikey.json", "r")
apikey = json.loads(f_apikey.read())
f_apikey.close()

YAHOO_API_URL = "http://jlp.yahooapis.jp/MAService/V1/parse"
YAHOO_API_ID = apikey["yahoo"]

GOOGLE_API_URL = "http://www.google.com/transliterate"
KIZASI_API_URL = "http://kizasi.jp/kizapi.py"

def nazokake(word):
  answers = []
  for because in get_related_words(word):
    if word in because or because in word:
      continue
    yomi = get_yomi(because)
    if yomi == u"いい":
      continue
    for homonym in get_homonyms(yomi):
      if word in homonym or homonym in word:
        continue
      if because in homonym or homonym in because:
        continue
      if homonym in yomi or yomi in homonym:
        continue
      for answer in get_related_words(homonym):
        if word in answer or answer in word:
          continue
        if answer in because or because in answer:
          continue
        if answer == u"いい":
          continue
        answers.append({
          "word": word,
          "answer": answer,
          "yomi": yomi,
          "because": because,
          "homonym": homonym
        })
  return answers

def get_related_words(word):
  words_w2v = aozora_sim.get_most_similar(word, 5)
  url = "%s?span=24&kw_expr=%s&type=coll" % (
      KIZASI_API_URL,
      word.encode("utf-8")
      )
  res = urllib2.urlopen(url)
  elemTree = fromstring(res.read())
  words_kizasi = list(i.text for i in elemTree.findall(".//title")[2:])
  return words_w2v + words_kizasi[:5]

def get_homonyms(word):
  url = "%s?langpair=ja-Hira|ja&text=%s" % (
        GOOGLE_API_URL,
        urllib.quote(word.encode("utf-8"))
      )
  res = urllib2.urlopen(url)
  p = json.loads(res.read())
  return p[0][1]

def get_yomi(word):
  url = "%s?appid=%s&sentence=%s" % (
        YAHOO_API_URL,
        YAHOO_API_ID,
        urllib.quote(word.encode("utf-8"))
      )
  res = urllib2.urlopen(url)
  elemTree = fromstring(res.read())
  kana = elemTree[0][2][0][1].text
  return kana

if __name__ == "__main__":
  import sys
  result = nazokake(sys.argv[1].decode("utf-8"))
  for i in result:
    print u"%sとかけまして%sとときます。" % (i["word"], i["answer"])
    print u"その心は"
    print u"どちらも%sがつきものです。" % i["yomi"]
    print u"-"*10
