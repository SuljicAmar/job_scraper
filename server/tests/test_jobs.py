import pytest
from datetime import datetime
from app.services.jobs import format_job, clean_urls
from app.models.jobs import MetaData, ParsedInfo, Job
from pydantic import ValidationError
from app.models.jobs import Job, MetaData, ParsedInfo

# ---- Create Fake Job Using Pydantic Models ----
FAKE_JOB = Job(
    url="https://jobs.example.com/job123",
    meta_data=MetaData(
        is_parsed=False, date_scraped=datetime.today().strftime("%m/%d/%Y")
    ),
    details=ParsedInfo(
        company_name="Example Corp",
        job_title="Data Scientist",
        location="Remote",
        job_type="Remote",
        minimum_salary=100000.0,
        maximum_salary=150000.0,
        salary="$100,000 - $150,000",
        responsibilities=["Analyze data", "Build models"],
        requirements=["Python", "SQL"],
        skills=["Python", "SQL", "Machine Learning"],
    ),
).model_dump()

# ---- Tests ----


def test_format_job_structure():
    result = format_job(FAKE_JOB)
    url_key = FAKE_JOB["url"]
    assert url_key in result
    assert "details" in result[url_key]
    assert result[url_key]["is_parsed"] is False
    assert result[url_key]["date_scraped"] == FAKE_JOB["meta_data"]["date_scraped"]


def test_clean_urls_removes_prefix_and_apply():
    urls = ["https://jobs.example.com/job123/apply", "https://jobs.example.com/job456"]
    cleaned = clean_urls(urls)
    assert cleaned == ["jobs.example.com/job123", "jobs.example.com/job456"]


def test_job_model_missing_required_fields():
    with pytest.raises(ValidationError):
        # Missing 'url' field which is required
        Job(
            meta_data=MetaData(is_parsed=True),
            details=ParsedInfo(
                company_name="Test",
                job_title="Engineer",
                location="Remote",
                job_type="Remote",
                minimum_salary=50000.0,
                maximum_salary=100000.0,
                salary="$50,000 - $100,000",
                responsibilities=["Work on projects"],
                requirements=["Python"],
                skills=["Python"],
            ),
        )


def test_parsed_info_invalid_job_type():
    with pytest.raises(ValidationError):
        # Invalid job_type that doesn't match the Literal values
        ParsedInfo(
            company_name="Test",
            job_title="Engineer",
            location="Remote",
            job_type="Contract",  # Invalid; should be 'Remote', 'Hybrid', 'Onsite', or 'Unknown'
            minimum_salary=50000.0,
            maximum_salary=100000.0,
            salary="$50,000 - $100,000",
            responsibilities=["Work on projects"],
            requirements=["Python"],
            skills=["Python"],
        )
