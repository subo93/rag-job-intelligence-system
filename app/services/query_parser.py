def parse_query(query: str):

    query = query.lower()

    filters = {
        "skill": None,
        "location": None,
        "salary": None
    }

    skills = [
        "python",
        "react",
        "javascript",
        "sql",
        "fastapi"
    ]

    for skill in skills:

        if skill in query:
            filters["skill"] = skill

    if "remote" in query:
        filters["location"] = "remote"

    if "high paying" in query:
        filters["salary"] = "high"

    return filters