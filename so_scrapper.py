import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

def get_last_page(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("a", {"class": "s-link"}).string
    company, location = html.find(
        "h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    uploading_day = html.find("span", {"class": "fc-orange-400"})
    company_img = html.find("img", {"class": "s-avatar--image"})
    if not company_img:
      company_img = "static/business.jpg"
    else:
      company_img =  company_img.get("src")
    return {"title": title, "company": company, "apply_link": f"https://stackoverflow.com/jobs/{job_id}", "location": location, "uploading": uploading_day, "company_img": company_img}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def so_get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs