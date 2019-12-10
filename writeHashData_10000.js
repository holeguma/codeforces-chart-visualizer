var SMALL = true; //小さいデータセットを作る時はtrueにする

var fs = require('fs');


var hash_data = JSON.parse(fs.readFileSync("./user_data/hash_data.json", 'utf8'));
var user_info = JSON.parse(fs.readFileSync("./user_data/user_info.json", 'utf8'));
var output = {};
var list = [];
var user_list = [];
async function calc_all() {
    var cnt = 0;
    for (key of Object.keys(user_info)) {
        //console.log(key);
        //console.log(user_info[key].rating);
        var obj = {};
        obj.userID = key;
        if (!user_info[key].rating) continue;
        obj.rating = user_info[key].rating;
        list.push(obj);
        cnt++;
    }
    list.sort(comp);
    for (var i = 0; i < 10000; i++) {
        var name = list[i].userID;
        if (name == 'holeguma') {
            console.log(name);
        }
        output[name] = hash_data[name];
    }

    function comp(a, b) {
        return b.rating - a.rating;
    }
}
calc_all().then(function() {
    var filename = './user_data/hash_data_10000.json';
    var json_data = JSON.stringify(output);
    fs.writeFileSync(filename, json_data);
})