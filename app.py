#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import random
import nazokake
import os
app = Flask(__name__, static_url_path="")

@app.route("/")
def index():
  return app.send_static_file("index.html")

@app.route("/js/<path:path>")
def js(path):
  return app.send_static_file(os.path.join("js", path))

@app.route("/css/<path:path>")
def css(path):
  return app.send_static_file(os.path.join("css", path))

@app.route("/nazokake/<string:word>", methods=["GET"])
def answer(word):
  answers = nazokake.nazokake(word)
  if len(answers) == 0:
    return jsonify([])
  answer = random.choice(answers)
  return jsonify(answer)

if __name__ == "__main__":
  app.run(debug  = True, port = 8888, host="172.21.32.73")
