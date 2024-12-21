import json
from datetime import datetime
from ..cfg import config
from ..models.jobs import MetaData, Job, Jobs

cfg = config()
path_to_jobs = cfg["path_to_jobs"]
job_site = cfg["job_site"]
scrape_search_engine = cfg["scrape"]


def format_job(job):
    return {
        job["url"]: {iKey: iVal for iKey, iVal in job["meta_data"].items()}
        | {"details": job["details"]}
    }


def create_new_jobs(job_urls):
    new_jobs = {}
    are_valid = clean_urls(job_urls)
    for iURL in are_valid:
        job_args = {
            "url": iURL,
            "meta_data": MetaData(
                **{
                    "is_parsed": False,
                    "date_scraped": datetime.today().strftime("%m/%d/%Y"),
                }
            ),
        }
        job = Job(**job_args).model_dump()
        new_jobs.update({job["url"]: format_job(job)[iURL]})
    return Jobs(**{"data": new_jobs})


def load_jobs():
    with open(path_to_jobs, "r") as file:
        jobs = json.load(file)
    return Jobs(**jobs)


def load_jobs_for_client():
    jobs = load_jobs().data
    return_arr = []
    for url, info in jobs.items():
        if info["is_parsed"]:
            temp_job = {"url": url}
            temp_job.update(info)
            return_arr.append(temp_job)
    return return_arr


def save_jobs(jobs):
    json_object = json.dumps(jobs.model_dump(), indent=4)
    with open(path_to_jobs, "w") as outfile:
        outfile.write(json_object)


def clean_urls(jobs):
    return [
        job.replace("https://", "").replace("/apply", "")
        for job in jobs
        if scrape_search_engine not in job
    ]
