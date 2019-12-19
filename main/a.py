import json

import requests

from main import db
from main.models import Problem, problem_tag


def update():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    data = response.json()
    n_problems = len(data["result"]["problems"])
    for i in range(n_problems):
        problem_info = data["result"]["problems"][i]
        problem = db.session.query(Problem).filter(
            Problem.name == problem_info['name']).first()
        if problem == None:
            new_problem = Problem(
                name=problem_info['name']
            )
            if "contestId" in problem_info:
                new_problem.contestID = problem_info["contestId"]
            if "index" in problem_info:
                new_problem.index = problem_info["index"]
            if "rating" in problem_info:
                new_problem.difficulty = problem_info["rating"]
            for tag in problem_info['tags']:
                new_problem.tags.append(db.session.query(
                    problem_tag).filter(problem_tag.name == tag).one())
            db.session.add(new_problem)
        print(str(i)+'/'+str(n_problems))
    db.session.commit()
