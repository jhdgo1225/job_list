import csv


def save_to_file(job_sites):
    file = open("jobs.csv", "w", encoding="utf-8-sig", newline='')
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for job_site in job_sites:
      for job in job_site:
        writer.writerow(list(job.values()))
