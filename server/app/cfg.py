# export PIP_REQUIRE_VIRTUALENV=true
# source .venv/bin/activate


def config():
    var_config = {
        "path_to_jobs": "./app/services/jobs.json",
        "scrape": "https://www.google.com/",
        "job_site": "jobs.lever.co",
    }
    var_config["query"] = f'(site:$1) (intitle:"data *") remote'.replace(
        "$1", var_config["job_site"]
    )
    return var_config
