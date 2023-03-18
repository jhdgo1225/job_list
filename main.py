"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""


from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import so_get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("start.html")

@app.route("/recommend")
def recommend():
  return render_template("recommend.html")

@app.route("/report")
def report():
  sites = []
  resultCount = 0
  word = request.args.get("word")
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      sites = existingJobs
    else:
      site_so = so_get_jobs(word)
      sites.append(site_so)
      db[word] = sites
    for job_site in sites:
        resultCount += len(job_site)
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word,
  resultsNumber=resultCount,
  so=sites[0])

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    job_sites = db.get(word)
    if not job_sites:
      raise Exception()
    save_to_file(job_sites)
    return send_file("jobs.csv")
  except:
    return redirect("/")
    

app.run(host="0.0.0.0")