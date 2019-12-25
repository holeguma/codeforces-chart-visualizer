import json
import os
from datetime import date, datetime, timedelta

import requests
from flask import render_template

from main import app, db
from main.models import Problem, User, problem_tag


def dumpFile(new_dir_path, new_filename, new_file_content, mode='w'):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(os.path.join(new_dir_path, new_filename), mode) as f:
        json.dump(new_file_content, f, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
        f.close()


@app.route('/')
def index():
    with open("main/user_data/hash_data_10000.json") as f:
        hash = json.load(f)
    with open("main/user_data/user_info.json") as f:
        user_info = json.load(f)
    with open("main/user_data/country_hash_data.json") as f:
        country_hash = json.load(f)
    return render_template('showRating.html', hash=hash, user_info=user_info, country_hash=country_hash)


@app.route('/ranking')
def ranking():
    with open("main/user_data/user_info.json") as f:
        user_info = json.load(f)
    with open("main/user_data/ranking_data_1000.json") as f:
        ranking_data = json.load(f)
    with open("main/user_data/country_ranking_data.json") as f:
        country_ranking_data = json.load(f)
    with open("main/user_data/country_code.json") as f:
        country_code = json.load(f)
    return render_template('showRanking.html', user_info=user_info, ranking_data=ranking_data, country_ranking_data=country_ranking_data, country_code=country_code)


@app.route('/userpage')
def userpage():
    return render_template('showUserPage.html')


@app.route('/userpage/<username>')
def getUserPage(username):
    # user = db.session.query(User).filter(User.name==username).first()
    # output = {}
    # if user == None:
    #     return render_template('showUserPage.html')
    # elif user.updated_at != date.today():
    #     user.difficulty_sum = 0
    #     user.cur_streak = 1
    #     user.max_streak = 1
    #     user.updated_at = date.today()
    #     url = "https://codeforces.com/api/user.status?handle=" + user.name + "&from=1&lang=en"
    #     response = requests.get(url)
    #     data = response.json()
    #     if data['status'] != 'OK':
    #         print(user.name)
    #         return
    #     n = len(data['result'])
    #     if n != 0:
    #         user.submission = data['result'][0]['id']
    #     lastAcceptedDate = None
    #     for i in reversed(range(n)):
    #         d = data['result'][i]
    #         if(d['verdict'] != 'OK'):
    #             continue
    #         if('contestId' not in d['problem'] or 'index' not in d['problem']):
    #             continue
    #         utc = datetime.utcfromtimestamp(d['creationTimeSeconds']).date()
    #         if utc-timedelta(days=1) == lastAcceptedDate:
    #             user.cur_streak += 1
    #         elif utc != lastAcceptedDate:
    #             user.max_streak = max(user.max_streak, user.cur_streak)
    #             user.cur_streak = 1
    #         lastAcceptedDate = utc
    #         problemID = str(d['problem']['contestId'])+d['problem']['index']
    #         # if(len(problemID)>=7):print(d)
    #         if not problemID in output:
    #             output[problemID] = 1
    #             problem = db.session.query(Problem).filter(
    #                 Problem.contestID == d['problem']['contestId'] and Problem.index == d['problem']['index']).first()
    #             if problem != None and problem.difficulty != None:
    #                 user.difficulty_sum += problem.difficulty
    #         # print(problemID)
    #     new_dir = './user_data/personal_data'
    #     filename = user.name+".json"
    #     dumpFile(new_dir, filename, output)
    #     print(user.id, user.name)
    #     user.max_streak = max(user.max_streak, user.cur_streak)
    #     if datetime.now().date()-timedelta(days=1) != lastAcceptedDate:
    #         user.cur_streak = 0
    #     db.session.commit()
    # hash={
    #     'rating': user.rating,
    #     'tags':[]
    # }
    
    # with open("main/user_data/rating_data/" + username + ".json") as f:
    #     rating_data = json.load(f)
    # return render_template('UserPage.html', name=username, hash=db.session.query(User).filter(User.name==username).first(), problem_list=db.session.query(Problem).all(), solved=len(output), rating_data=rating_data['result'],  difficultySum=user.difficulty_sum)
    with open("main/user_data/hash_data_10000.json") as f:
        hash = json.load(f)
    with open("main/problem_data/problem_list.json", encoding="utf-8") as f:
        data = json.load(f)
    problem_list = []
    with open("main/user_data/personal_data/" + username + ".json") as f:
        solved = json.load(f)
    difficultySum=0
    for problem in solved:
        contestID=-1
        problem_index=-1
        if problem[-1:].isdigit():
            contestID=int(problem[:-2])
            problem_index=problem[-2:]
        else:
            contestID=int(problem[:-1])
            problem_index=problem[-1:]
        list=[x for x in data['result']['problems'] if x['contestId']==contestID and x['index']==problem_index]
        if len(list) and 'rating' in list[0]:
            difficultySum+=list[0]['rating']
        for i in range(len(data['result']['problems'])):
            if '"' in data['result']['problems'][i]['name'] or '%' in data['result']['problems'][i]['name']:
                continue
            problem_list.append(data['result']['problems'][i])
    with open("main/user_data/rating_data/" + username + ".json") as f:
        rating_data = json.load(f)
    with open("main/user_data/user_info.json") as f:
        user_info = json.load(f)
    return render_template('UserPage.html', name=username, hash=hash[username], problem_list=problem_list, solved=solved, rating_data=rating_data['result'], user_info=user_info,difficultySum=difficultySum)