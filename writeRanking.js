var fs = require('fs');

var cnt = 0;
let n_contests = 1260;

var hash = {};
var ranking = {};
var data = JSON.parse(fs.readFileSync("./user_data/small_hash_data.json", 'utf8'));
hash = JSON.parse(JSON.stringify(data));
var n_users = Object.keys(hash).length;
//console.log(n_users);
var names = Object.keys(hash);

function compare(u1, u2) {
    if (u1.rating < u2.rating) return 1;
    else return -1;
}
async function makeRanking() {
    for (var i = 0; i < n_users; i++) {
        for (tag in hash[names[i]].tags) {
            //console.log(tag);
            if (!ranking[tag]) {
                ranking[tag] = [];
            }
            ranking[tag].push({
                rank: 0,
                userID: names[i],
                rating: Math.round(hash[names[i]]["tags"][tag].value),
                solved: hash[names[i]]["tags"][tag].solveCount
            });
            //console.log(ranking[tag]);
        }
        //console.log(hash[names[i]]);Node 
    }
    for (tag in ranking) {
        console.log(tag);
        ranking[tag].sort(compare);
        for (var i = 0; i < ranking[tag].length; i++) {
            ranking[tag][i].rank = i + 1;
        }
    }
}

makeRanking().then(function() {
    var json_data = JSON.stringify(ranking);
    fs.writeFileSync('./user_data/small_ranking_data-2.json', json_data);
})