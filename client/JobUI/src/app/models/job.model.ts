export interface Job {
    url: string;
    date_scraped: string;
    is_parsed: boolean;
    details: JobDetails

}

export interface JobDetails {
    company_name: string;
    job_title: string;
    job_type: string;
    location: string;
    minimum_salary: number;
    maximum_salary: number;
    requirements: string[];
    responsibilities: string[];
    salary: string;
    skills: string[];
}