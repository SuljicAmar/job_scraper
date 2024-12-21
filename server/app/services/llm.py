from ollama import generate


def ask_ai(system_prompt, user_prompt, job_schema):
    response = generate(
        model="llama3.2",
        system=system_prompt,
        prompt=user_prompt,
        format=job_schema.model_json_schema(),
        options=llm_options(),
    )
    response = job_schema.model_validate_json(response.response)
    return response


def llm_options():
    return {"temperature": 0.3, "num_ctx": 10000}


def parse_job_reqs():
    return """You are an expert in exhaustively parsing and categorizing provided
      job postings into individual componenets. Use deductive reasoning and summarize as needed
       to create a conscise breakdown of the job in an easily accessible, filterable, and searchable format. \n"""
