# Information Visualization
## Codeforcesのレート計算式について
### 定義
* $n$ : コンテスト参加者の数
* $r_i$ : $i$番目の参加者の変更前のRating
* $rank_i$ : $i$番目の参加者の順位
* $P_{i,j}$ : $i$番目の参加者が$j$番目の参加者よりいい結果を出せる確率
  $P_{i,j}=\cfrac{1}{1+10^{\frac{r_i-r_j}{400}}}$
* $seed_i$ : $i$番目の参加者のSeed値
  $seed_i=\displaystyle\sum _{j=1 \\ i\neq j}^{n} P_{j,i}+1$
* $d_i$ : $i$番目の参加者のレート変動
* $s$ : そのコンテストでレート変動に補正を行うべき人数
### 手順
1. 参加者の順位を確定
2. 参加者のSeed値$seed_i$を計算
3. $m_i=\sqrt{seed_i\times rank_i}$を計算
4. 実際の実力$R_i$を全参加者とのSeed値が$m_i$となるようなRatingの値とする[^1]
5. $d_i=\cfrac{R_i-r_i}{2}$をレート変動とする
6. コンテスト上位[^2]のRatingが上がりすぎるのを防ぐため、上位$s$人に対して$d_i+=min(max(-sum_s/s,-10),0)$の補正を行う。


[^1]:全参加者とのSeed値はRatingに対して単調性があるので二分探索を用いて求めることができる
[^2]:具体的にはそのコンテストの上位$min(4\times round(\sqrt{n}),n)$位まで