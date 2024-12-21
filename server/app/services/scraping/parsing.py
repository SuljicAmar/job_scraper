from .sites import Lever
from ..llm import ask_ai, parse_job_reqs
from ...models.jobs import ParsedInfo, Jobs
from ..jobs import save_jobs


def parse_lever_postings(jobs):
    lever_parser = Lever()
    return lever_parser.parse_jobs(jobs)


def parse_using_ai(posting_req):
    return ask_ai(parse_job_reqs(), posting_req, ParsedInfo)


def parse_and_save_lever(jobs):
    try:
        descs = parse_lever_postings(jobs)
        parsed_jobs = {}
        for k, v in descs.items():
            ai_parsed = parse_using_ai(v)
            jobs[k]["details"].update({"minimum_salary": ai_parsed.minimum_salary})
            jobs[k]["details"].update({"maximum_salary": ai_parsed.maximum_salary})
            jobs[k]["details"].update({"salary": ai_parsed.salary})
            jobs[k]["details"].update({"responsibilities": ai_parsed.responsibilities})
            jobs[k]["details"].update({"requirements": ai_parsed.requirements})
            jobs[k]["details"].update({"skills": ai_parsed.skills})
            jobs[k].update({"is_parsed": True})
    except Exception as exception:
        del jobs[k]
    finally:
        save_jobs(Jobs(**{"data": jobs}))
