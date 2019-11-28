import json
from time import sleep

import requests
from tqdm import tqdm

contestId = 566
count = 5  # 十分大きくすると参加者全員とれるらしい
url = "https://codeforces.com/api/contest.standings?contestId=" + \
    str(contestId)+"&from=1&count="+str(count)+"&showUnofficial=true"
response = requests.get(url)
json_data = response.json()


def getData(count=5):
    res=[]
    #新しくディレクトリを作ってここにデータを保存する
    new_dir='./'+str(datetime.datetime.today().strftime("%Y%m%d"))
    os.makedirs(new_dir, exist_ok=True)
    
    for contestId in tqdm(range(1,count+1)):
        #print("contestId : "+str(contestId))
        filename=str(contestId)+'.json'
        url="https://codeforces.com/api/contest.standings?contestId="+str(contestId)+"&from=1&count="+str(count)+"&showUnofficial=true"
        response=requests.get(url)
        json_data=response.json()
        
        dumpFile(new_dir,filename,json_data)
        res.append(json_data)
        if not contestId%5:
            sleep(1.5)
        #print(res)
        
    return res


data = getData()
