import json

def load_jobs():

    with open("app/data/jobs.json", "r") as file:

        jobs = json.load(file)

    return jobs