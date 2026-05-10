import json

def load_jobs():

    with open("app/data/jobs.json", "r") as file:

        jobs = json.load(file)

    return jobs

def search_jobs(skill: str):

    jobs = load_jobs()

    results = []

    for job in jobs:

        skills = [s.lower() for s in job["skills"]]

        if skill.lower() in skills:

            results.append(job)

    return results

def format_jobs_context(jobs):

    context = ""

    for job in jobs:

        context += f"""
        Job Title: {job['title']}
        Skills: {', '.join(job['skills'])}
        Salary: {job['salary']}
        Location: {job['location']}

        """

    return context