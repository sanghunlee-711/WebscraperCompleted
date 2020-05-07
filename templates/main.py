from flask import Flask, render_template, request, redirect, send_file
from scraper import get_jobs
from exporter import save_to_file
app = Flask("WebScrapper")

db = {} 

@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower() #대문자 입력시 소문자 변환용
    existingJobs = db.get(word)
    if existingJobs:
      jobs = []
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")# 미입력시 홈으로 redirect
  return render_template(
    "report.html",
    searchingBy=word,
    resultsNumber=len(jobs),
    jobs=jobs) 
    #jobs는 array니까 length


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()  
    save_to_file(jobs)  
    return send_file("jobs.csv") 
  except:
    return redirect("/")
"""
jobs를 fake db에서 가져옴 거기에 해당 jobs가 없으면 또 Exception으로 보냄
"""
"""
try블록안의 exception한 사항이 있으면 except 문 안의 redirect가 실행이 됨.
만약 word가 존재하지 않으면 exception(==error)을 발생시키고 except: 블록으로가서 return redirect("/")를
실행하는 구조
"""


app.run(host="0.0.0.0") 

