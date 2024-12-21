from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from datetime import datetime


class ParsedInfo(BaseModel):
    company_name: str
    job_title: str
    location: str
    job_type: Literal["Remote", "Hybrid", "Onsite", "Unknown"]
    minimum_salary: float
    maximum_salary: float
    salary: str
    responsibilities: List[str]
    requirements: List[str]
    skills: List[str]


class MetaData(BaseModel):
    is_parsed: bool = False
    date_scraped: str = Field(
        default_factory=lambda x: datetime.today().strftime("%m/%d/%Y")
    )


class Job(BaseModel):
    url: str
    meta_data: MetaData
    details: Optional[ParsedInfo] = ParsedInfo(
        **{
            "company_name": "",
            "job_title": "",
            "location": "",
            "job_type": "Unknown",
            "minimum_salary": 0.0,
            "maximum_salary": 0.0,
            "salary": "$0 - 0",
            "responsibilities": ["None"],
            "requirements": ["None"],
            "skills": ["None"],
        }
    )


class Jobs(BaseModel):
    data: Dict[str, Dict]
