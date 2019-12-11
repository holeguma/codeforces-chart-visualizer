import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open("./user_data/hash_data_10000.json") as f:
        hash = json.load(f)
    with open("./user_data/user_info.json") as f:
        user_info = json.load(f)
    with open("./user_data/country_hash_data.json") as f:
        country_hash = json.load(f)
    return render_template('showRating.html', hash=hash, user_info=user_info, country_hash=country_hash)


@app.route('/ranking')
def ranking():
    with open("./user_data/user_info.json") as f:
        user_info = json.load(f)
    with open("./user_data/ranking_data_1000.json") as f:
        ranking_data = json.load(f)
    with open("./user_data/country_ranking_data.json") as f:
        country_ranking_data = json.load(f)
    with open("./user_data/country_code.json") as f:
        country_code = json.load(f)
    return render_template('showRanking.html', user_info=user_info, ranking_data=ranking_data, country_ranking_data=country_ranking_data, country_code=country_code)


@app.route('/userpage')
def userpage():
    return render_template('showUserPage.html')


@app.route('/userpage/<username>')
def getUserPage(username):
    with open("./user_data/hash_data_10000.json") as f:
        hash = json.load(f)
    with open("./problem_data/problem_list.json", encoding="utf-8") as f:
        data = json.load(f)
    problem_list = []
    with open("./user_data/personal_data/" + username + ".json") as f:
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
        if len(list):
            difficultySum+=list[0]['rating']

    for i in range(len(data['result']['problems'])):
        if '"' in data['result']['problems'][i]['name'] or '%' in data['result']['problems'][i]['name']:
            continue
        problem_list.append(data['result']['problems'][i])
    with open("./user_data/rating_data/" + username + ".json") as f:
        rating_data = json.load(f)
    with open("./user_data/user_info.json") as f:
        user_info = json.load(f)
    return render_template('UserPage.html', name=username, hash=hash[username], problem_list=problem_list, solved=solved, rating_data=rating_data['result'], user_info=user_info,difficultySum=difficultySum)


if __name__ == '__main__':
    app.run()
