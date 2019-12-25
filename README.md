# Information Visualization

## contest_data
[Google Drive](https://drive.google.com/open?id=1q_qYlU_8CXlPlPt0KQPVpBp6f18PrVkB)からダウンロードしてください

## calcRating.html
`contest_data`フォルダと`lib/d3.js`を同じ階層において実行してください<br>
↑<br>
d3をurlからとってくるようにしたから大丈夫です。

## user_data
`user_data`内の`hash_data.zip`と`user_list.zip`はファイルサイズが大きいので圧縮してあります

## template
このディレクトリにhtmlファイルを配置して下さい

## static
このディレクトリにjs/cssファイルを配置して下さい

## Requirement
```
pip install Flask Jinja2 werkzeug
```

## Usage
b-piyomboディレクトリ直下で
```
python run.py
```
を実行して http://localhost:5000/ にアクセスすると結果が見れます。
