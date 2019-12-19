import json
import os
from datetime import date, datetime, timedelta
from time import sleep

import requests

from main import db
from main.models import (
    Country, Problem, User, country_tag, finished_contest, user_tag)


def updateRating(rating, difficulty, wins, loses, K):
    if rating - difficulty > 800 and wins == 0 and loses == 1:
        return rating
    games = wins + loses
    winProbability = 1.0 / ((10.0**((difficulty - rating) / 400.0)) + 1.0)
    newRating = rating + K * (wins - games*winProbability)
    return newRating


def update():
    all_tags = ["bitmasks", "divide and conquer", "math", "data structures", "trees", "dp", "greedy", "binary search", "sortings", "number theory", "fft", "brute force", "hashing", "meet-in-the-middle", "two pointers", "implementation", "strings", "constructive algorithms", "graphs",
                "combinatorics", "dfs and similar", "dsu", "probabilities", "geometry", "interactive", "ternary search", "shortest paths", "flows", "matrices", "2-sat", "graph matchings", "games", "*special", "string suffix structures", "expression parsing", "chinese remainder theorem", "schedules"]
    contestID = 80
    while True:
        finished = db.session.query(finished_contest).filter(
            finished_contest.contestID == contestID).first()
        if finished != None:
            contestID += 1
            continue
        url = 'https://codeforces.com/api/contest.standings?showUnofficial=false&contestId=' + \
            str(contestID)
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'FAILED':
            print(str(contestID)+' : FAILED')
            if data['comment'][-2] == 'n':
                break
            else:
                contestID += 1
                continue
        print(str(contestID)+' : OK')
        problems = data['result']['problems']
        n_problems = len(problems)
        ranks = data['result']['rows']
        n_contestants = len(ranks)
        if not n_contestants:
            contestID += 1
            continue
        for j in range(n_problems):
            difficulty = problems[j]['rating']
            if not difficulty:
                continue
            country_result = {}
            all_countries = db.session.query(Country).all()
            for country in all_countries:
                country_result[country.name] = {}
                for tag in all_tags:
                    country_result[country.name][tag] = {
                        'wins': 0,
                        'loses': 0
                    }
            for i in range(n_contestants):
                print(str(contestID)+' : '+str(j)+' : '+str(i))
                result = 1 if ranks[i]['problemResults'][j]['points'] else 0
                name = ranks[i]['party']['members'][0]['handle']
                if ranks[i]['party']['participantType'] != 'CONTESTANT':
                    continue
                user = db.session.query(User).filter(User.name == name).first()
                if not user:
                    continue
                if not user.tags:
                    for tag in all_tags:
                        user.tags.append(user_tag(
                            name=tag,
                            rating=1500,
                            solved=0
                        ))
                    db.session.commit()
                for tag in problems[j]['tags']:
                    utag = db.session.query(user_tag).filter(
                        user_tag.user_id == user.id, user_tag.name == tag).first()
                    K = 64
                    if utag.solved < 10:
                        K *= (10 - utag.solved)
                    rating = utag.rating
                    utag.rating = updateRating(
                        rating, difficulty, result, result ^ 1, K)
                    utag.solved += result
                if not user.country:
                    continue
                print(user.country)
                for tag in problems[j]['tags']:
                    if result:
                        country_result[user.country][tag]['wins'] += 1
                    else:
                        country_result[user.country][tag]['loses'] += 1
            for country in all_countries:
                for tag in problems[j]['tags']:
                    ctag = db.session.query(country_tag).filter(
                        country_tag.country_id == country.id, country_tag.name == tag).first()
                    rating = ctag.rating
                    ctag.rating = updateRating(
                        rating, difficulty, country_result[country.name][tag]['wins'], country_result[country.name][tag]['loses'], 0.5)
                    ctag.solved += country_result[country.name][tag]['wins']
            db.session.commit()
        finished = finished_contest(
            contestID=contestID
        )
        contestID += 1
        db.session.add(finished)
        db.session.commit()
