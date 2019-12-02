
var SMALL = false;//小さいデータセットを作る時はtrueにする

var fs = require('fs');
let n_contests = 1260;
//自分のrating,問題のdifficulty,解けたかどうか, から新しいratingを計算する
function updateRating(rating, difficulty, result, K = 64) {
    if (rating - difficulty > 800 && result == 0) return rating;
    var winProbability = 1.0 / (Math.pow(10.0, (difficulty - rating) / 400.0) + 1.0);
    var newRating = rating + K * (result - winProbability);
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
        for (let i = 0; i < (SMALL) ? 100 : n_contestants; i++) {
            let name = ranks[i].party.members[0].handle;
            if (ranks[i].party.participantType != 'CONTESTANT') continue; // Contestantでなければスキップ
            //もしハッシュに名前が登録されてなければ新しく作る
            if (!hash[name]) {
                hash[name] = JSON.parse(JSON.stringify(Status));
                hash[name].userID = name;
                if (country_hash[name]) {
                    hash[name].country = country_hash[name];
                }
            }
            if (DEBUG && name == showID) {
                console.log(data.result.problems);
                console.log(ranks[i].problemResults);
                console.log(hash[name]);
            }
            for (let j = 0; j < n_problems; j++) {
                let result = ranks[i].problemResults[j].points ? 1 : 0;
                let difficulty = problems[j].rating;
                if (!difficulty) continue; //問題にdifficultyが設定されてなければスキップ
                for (let tag of problems[j].tags) {
                    if (tag == name) continue;
                    let rating = hash[name]["tags"][tag].value;
                    var K = 64;
                    //そのタグの問題を解いた回数が少なければレート変化を大きくする
                    if (hash[name]["tags"][tag].solveCount < 10) K *= (10 - hash[name]["tags"][tag].solveCount);
                    hash[name]["tags"][tag].value = updateRating(rating, difficulty, result, K);
                    if (DEBUG && name == showID) {
                        console.log(tag + ":" + rating + "->" + hash[name]["tags"][tag].value);
                    }
                    if (result) hash[name]["tags"][tag].solveCount++;
                }
            }
        }
        resolve();
    })
}

async function calc_all() {
    for (let i = (SMALL) ? 1230 : 1; i <= n_contests; i++) {
        var result = await calcRating(i);
    }
}

var data = JSON.parse(fs.readFileSync("./user_data/user_info.json", 'utf8'));

country_hash = JSON.parse(JSON.stringify(data));
calc_all().then(function () {
    console.log(hash["Mojumbo"]);
    console.log(hash["holeguma"]);
    console.log(hash["tourist"]);
    console.log(hash["rng_58"]);
    console.log(hash["ransewhale"]);
    console.log(hash["QWE_QWE"]);
    console.log(hash["totori0908"]);
    console.log(hash["Rubikun"]);
})
    .then(function () {
        var filename = './user_data/' + ((SMALL) ? "small_" : "") + "hash_data.json";
        var json_data = JSON.stringify(hash);
        fs.writeFileSync(filename, json_data);
    })


