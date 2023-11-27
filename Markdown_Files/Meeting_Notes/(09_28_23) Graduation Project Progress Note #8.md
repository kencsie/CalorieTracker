# 組員
* 411021391 張晉睿
* 411021312 張愷恩
* 411021342 Kenrick Albert
* 411021365 Nguyễn Minh Trang

# 本次會議內容
- 講好這次版本的系統架構 (Explained the most recent iteration of the arhitecture diagram)
- 跟助教講好食物卡路里論文 (Introduced supplementary papers for the calorie estimation system)
 
# TA recommendation(English)
## Paper introduction
1) How did you obtain the dataset for this model/training? If we train our own dataset, how did we uitilize it within the project?
2)  What are the inputs and outputs of these systems. Outline the methods for obtaining an acceptable output (Requires consultation with Professor)
## Difference
1) Has this exact thing been done already?
2) How does our system differ from other popular systems?
3) Is there already an application on the market with similar functionality? If so, what would be the benefit of continuing this particular research topic?
## Recommendation System
1) How did you connect the calorie estimation system to the recommender system? (Must support proper pipelining)
2) Why did you use this type of model (BERT) as opposed to ChatGPT to facilitate the recommender system?
     
# 研究生的建議(中文)
## 介紹論文
1) 何處取得用於訓練的資料集? 要如何使用資料集訓練? 提供準備資料集的方法
2) 系統的輸入/輸出為何?介紹得出可行結果的方法(與教授討論)

## 差別
1) 這個已經做過了嗎?
2) 我們提出的系統與其他人的有什麼差別?
3) 市面上相似的應用程式嗎? 如果有，我們的應用程式與其他的有什麼不同?

## 推薦系統
1) 如何連接計算卡路里系統與推薦系統? (提供適當的連接方式)
2) 在推薦系統中，為什麼不使用ChatGPT而使用Bert?

# 會後討論
-
  
# 下周進度(next week schedule)
- Question & Answer for NLP
- Fine Tuning for Machine Learning Models

# 重要的通知(Important notification)
- Meeting with TA, October 2 @ 7PM (Online)
- Meeting with professor (requires Slideshow Presentation)
- Ideal division of labour
- Track our progress within a Gantt Chart (from this time onwards)

# 我們架構的不同(中文)

![](https://hackmd.io/_uploads/S1SwGQde6.png)

## 資料集

這個資料集是別人預先建立的，裡面包含著四種角度拍攝食物的影片，也有每個餐盤的質量、卡路里資訊，以及食材種類
https://github.com/google-research-datasets/Nutrition5k#download-data

## 推薦系統
https://ieeexplore.ieee.org/document/9775081
### 輸入/輸出
輸入為用戶對部分食物的評分
輸出為推薦食物的串列(根據最適合的食物排序)
### 架構
1. FOOD DEEP EMBEDDING
    使用Bert將食物中的食材，轉變成n維度的embedding
2. FOOD SIMILARITY CALCULATION
    計算兩個食物的差距
3. FOOD CLUSTERING
    使用Deep Embedded Clustering的技巧，把關聯的食物聚集
### 資料集
使用爬蟲爬取 Allrecipes.com
>  In total, 68,768 users, 45,630 foods with 33,147 ingredients, and 1,093,845 ratings were collected.
### 準確度
<img src="https://hackmd.io/_uploads/rJD17-uep.png" width="400px">
<img src="https://hackmd.io/_uploads/Syqxm-dg6.png" width="400px">

### 目前的問題
1. 此篇論文只有參考食物的原料
2. 沒有與計算卡路里模型連結的部分


## 獨特之處
1.除此之外，我們查看過其他市面上的app，有些app計算食物卡路里要付費，而免費的則是結果不好，我們想要提出一個更準確且輕量的系統，幫助使用者管理健康飲食

2.我們除了在食物卡路里外，還加上了推薦系統，希望能幫使用者自動依據他所選擇的食物，規劃他明天的餐點

# 小組分工(Division of labour)

# 時程
![](https://hackmd.io/_uploads/S1eD4QOxp.png)


# 相關連結
[專題進度目錄](https://hackmd.io/_67oi56gQ-6nhA-f69g5AA?both)
[食物卡路里論文整理](https://hackmd.io/HrTIye29RTegtYsO8Yx62A)
