import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open("./user_data/small_hash_data.json") as f:
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
    with open("./user_data/small_hash_data.json") as f:
        hash = json.load(f)
    return render_template('UserPage.html', name=username, hash=hash[username])


if __name__ == '__main__':
    app.run()
