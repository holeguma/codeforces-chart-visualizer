
var fs = require('fs');
let n_contests = 1260;
//自分のrating,問題のdifficulty,解けたかどうか, から新しいratingを計算する
function updateRating(rating, difficulty, wins, loses, K = 0.5) {
    // console.log(rating + " " + difficulty + " " + wins + " " + loses + " " + K);
    var games = wins + loses;
    var winProbability = 1.0 / (Math.pow(10.0, (difficulty - rating) / 400.0) + 1.0);
    var newRating = rating + K * (wins - games * winProbability);
    return newRating;
}
//ユーザーネーム→国名のハッシュ
country_hash = {};
//ユーザーネーム→各タグのrating のハッシュを用意する
var hash = {};

const Status = {
    userID: "sample",
    country: "unknown",
    tags: {
        "bitmasks": {
            value: 1500,
            solveCount: 0
        },
        "divide and conquer": {
            value: 1500,
            solveCount: 0
        },
        "math": {
            value: 1500,
            solveCount: 0
        },
        "data structures": {
            value: 1500,
            solveCount: 0
        },
        "trees": {
            value: 1500,
            solveCount: 0
        },
        "dp": {
            value: 1500,
            solveCount: 0
        },
        "greedy": {
            value: 1500,
            solveCount: 0
        },
        "binary search": {
            value: 1500,
            solveCount: 0
        },
        "sortings": {
            value: 1500,
            solveCount: 0
        },
        "number theory": {
            value: 1500,
            solveCount: 0
        },
        "fft": {
            value: 1500,
            solveCount: 0
        },
        "brute force": {
            value: 1500,
            solveCount: 0
        },
        "hashing": {
            value: 1500,
            solveCount: 0
        },
        "meet-in-the-middle": {
            value: 1500,
            solveCount: 0
        },
        "two pointers": {
            value: 1500,
            solveCount: 0
        },
        "implementation": {
            value: 1500,
            solveCount: 0
        },
        "strings": {
            value: 1500,
            solveCount: 0
        },
        "constructive algorithms": {
            value: 1500,
            solveCount: 0
        },
        "graphs": {
            value: 1500,
            solveCount: 0
        },
        "combinatorics": {
            value: 1500,
            solveCount: 0
        },
        "dfs and similar": {
            value: 1500,
            solveCount: 0
        },
        "dsu": {
            value: 1500,
            solveCount: 0
        },
        "probabilities": {
            value: 1500,
            solveCount: 0
        },
        "geometry": {
            value: 1500,
            solveCount: 0
        },
        "interactive": {
            value: 1500,
            solveCount: 0
        },
        "ternary search": {
            value: 1500,
            solveCount: 0
        },
        "shortest paths": {
            value: 1500,
            solveCount: 0
        },
        "flows": {
            value: 1500,
            solveCount: 0
        },
        "matrices": {
            value: 1500,
            solveCount: 0
        },
        "2-sat": {
            value: 1500,
            solveCount: 0
        },
        "graph matchings": {
            value: 1500,
            solveCount: 0
        },
        "games": {
            value: 1500,
            solveCount: 0
        },
        "*special": {
            value: 1500,
            solveCount: 0
        },
        "string suffix structures": {
            value: 1500,
            solveCount: 0
        },
        "expression parsing": {
            value: 1500,
            solveCount: 0
        },
        "chinese remainder theorem": {
            value: 1500,
            solveCount: 0
        },
        "schedules": {
            value: 1500,
            solveCount: 0
        }
    }
};

var DEBUG = false;
var showID = "tourist";
//コンテストIDから、参加者全員のratingを更新する
function calcRating(contestID) {
    return new Promise((resolve, reject) => {
        var filename = "./contest_data/" + contestID + ".json";
        var data = JSON.parse(fs.readFileSync(filename, 'utf8'));
        //console.log(data);
        //コンテストデータがなければスキップ
        if (data.status == "FAILED") {
            console.log(contestID + ":FAILED");
            return resolve();
        } else {
            console.log(contestID + ":OK");
        }
        let problems = data.result.problems;
        let n_problems = problems.length;

        let ranks = data.result.rows;
        let n_contestants = ranks.length;
        if (!n_contestants) return resolve();
        var countProblems = {};

        for (let i = 0; i < n_contestants; i++) {
            let name = ranks[i].party.members[0].handle;
            if (ranks[i].party.participantType != 'CONTESTANT') continue; // Contestantでなければスキップ
            //もしハッシュに名前が登録されてなければ新しく作る
            if (!country_hash[name]) continue;
            var country = country_hash[name];
            if (!hash[country]) {
                hash[country] = JSON.parse(JSON.stringify(Status));
                hash[country].country = country;
                hash[country].userID = country;
            }
            if (!countProblems[country]) countProblems[country] = {};
            for (let j = 0; j < n_problems; j++) {
                let problemID = problems[j].index;
                if (!countProblems[country][problemID]) countProblems[country][problemID] = {
                    "win": 0,
                    "lose": 0
                };
                let result = ranks[i].problemResults[j].points ? 1 : 0;
                let difficulty = problems[j].rating;
                if (!difficulty) continue; //問題にdifficultyが設定されてなければスキップ
                for (let tag of problems[j].tags) {
                    if (result) {
                        countProblems[country][problemID].win++;
                    } else countProblems[country][problemID].lose++;
                }
            }
        }
        for (country in countProblems) {
            for (var j = 0; j < n_problems; j++) {
                var problemID = problems[j].index;
                let difficulty = problems[j].rating;
                if (!difficulty) continue;
                for (let tag of problems[j].tags) {
                    var rating = hash[country]["tags"][tag].value;
                    if (!countProblems[country]) {
                        console.log(country);
                    }
                    var wins = countProblems[country][problemID].win;
                    var loses = countProblems[country][problemID].lose;
                    hash[country]["tags"][tag].solveCount += wins;
                    hash[country]["tags"][tag].value = updateRating(rating, difficulty, wins, loses);
                }
            }
            //if (country == "Japan") console.log(hash[country]);
        }
        resolve();
    })
}

async function calc_all() {
    for (let i = 1; i <= n_contests; i++) {
        var result = await calcRating(i);
    }
}

var data = JSON.parse(fs.readFileSync("./user_data/country_list.json", 'utf8'));

country_hash = JSON.parse(JSON.stringify(data));
calc_all().then(function () {
    console.log(hash["China"]);
    console.log(hash["Japan"]);
    console.log(hash["Tunisia"]);
    console.log(hash["Bangladesh"]);
    console.log(hash["India"]);
    console.log(hash["Belarus"]);
})
    .then(function () {
        var filename = './user_data/' + "country_hash_data.json";
        var json_data = JSON.stringify(hash);
        fs.writeFileSync(filename, json_data);
    })


