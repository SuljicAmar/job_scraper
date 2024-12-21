import requests
from bs4 import BeautifulSoup


class Lever:

    def __init__(self):
        self.site = "jobs.lever.co"

    def parse_jobs(self, jobs):
        if not jobs:
            return jobs
        job_descs = {}
        for iKey, iValue in jobs.items():
            if iValue["is_parsed"] or self.site not in iKey:
                continue
            source = self.get_source(iKey)
            iValue["details"].update(self.company_and_title(source))
            if (
                iValue["details"]["company_name"] == ""
                and iValue["details"]["job_title"] == ""
            ):
                continue
            iValue["details"].update(self.job_type(source))
            iValue["details"].update(self.location(source))
            job_descs.update({iKey: self.posting_text(source)})
        return job_descs

    def get_source(self, url):
        if "https://" not in url:
            url = f"https://{url}"
        return BeautifulSoup(requests.get(url).content, "html.parser")

    def company_and_title(self, source):
        try:
            title = source.find("title").text.split("-")
            return {"company_name": title[0].strip(), "job_title": title[1].strip()}
        except Exception as e:
            return {"company_name": "", "job_title": ""}

    def job_type(self, source):
        try:
            if "remote" in source.find("title").text.lower():
                return {"job_type": "Remote"}
            return {
                "job_type": source.find("div", class_="workplaceTypes").text.rstrip("/")
            }
        except Exception as e:
            return {"job_type": "Unknown"}

    def location(self, source):
        try:
            return {"location": source.find("div", class_="location").text.rstrip("/")}
        except Exception as e:
            return {"location": ""}

    def posting_text(self, source):
        try:
            job_desc = source.find_all("div", class_="section page-centered")
            return "".join([f" \n {i.text} \n " for i in job_desc])
        except Exception as e:
            return None
