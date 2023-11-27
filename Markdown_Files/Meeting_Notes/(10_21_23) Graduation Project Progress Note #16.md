# 組員
* 411021391 張晉睿
* 411021312 張愷恩
* 411021342 Kenrick Albert
* 411021365 Nguyễn Minh Trang

# 分工 (Division of Labour)
### 推薦系統 Recommender System
- Understand more in LLM: Ken & Kenrick
    - How to get finetune work
- Feasibility of Paper (Testing of Code): Ken
    - The actual input and output of the paper
- General Research (Paper Concepts): Ken & Kenrick
    - Research on the concepts mentioned in the paper (SRL, etc.)
    - look on the reference of the UniSRec

### 營養系統 Nutrition System
#### Training of Model & Alternative Resources
- YOLO V5: Trang
- YOLO V4: Jimmy

## 簡單介紹(論文實作)
### 使用的資料
這邊使用了amazon的[爬取資料](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/)

有兩種資料
1. Metadata
    商品的簡介
    :::spoiler 範例
    {"category": ["Video Games", "Retro Gaming & Microconsoles", "Game Boy Advance", "Games"], "tech1": "", "description": ["Re-released in celebration of the 25th anniversary of the Nintendo entertainment system console, Super Mario Bros. brings you back to the first epic battle between Mario and Bowser. Relive the mushroom-eating, Koopa-stomping action, and Mario's merciless jumping as you enjoy a great classic from the early days of Nintendo. Comes in a standard Game Boy Advance box featuring the classic artwork of the original game.", "<P>Admit it. You played it. You loved it. It might have been that first game that made you realize what was coming in this little hobby of ours. This is a perfect port of the original Super Mario Bros. Every last mushroom and goomba is accounted for, and you'll feel yourself slipping into a blissful recollection of your early days as a gamer. Just don't expect anything revolutionary here. The closest thing to newness is the ability to link up with another GBA to play with a friend, but don't worry. Two-player is still available on just one unit. If you're looking for innovation, check out the excellent Deluxe version on Game Boy Color. But for purists, this is the cream of the crop in retro goodness. So, if you're willing to drop the 20 gold coins for this one, enjoy your trip down memory lane.<BR><BR>Rated: <B>9 out of 10</B><BR>Editor: <B>Matt Miller</B><BR>Issue: <B>June 2004</B><BR><BR><BR><BR><a href=\"http://www.amazon.com/exec/obidos/ASIN/B0000AN45D/\" target=\"\"><img src=\"https://images-na.ssl-images-amazon.com/images/G/01/videogames/logos/gi_logo.gif\" border=\"0\"></a><BR><a href=\"http://www.amazon.com/exec/obidos/ASIN/B0000AN45D/\">Subscribe to Game Informer</a> -- <i>Game Informer Review</i>"], "fit": "", "title": "Super Mario Bros. - Classic NES Series", "also_buy": ["B00009WAUO", "B00005UK88", "B00005B8FZ", "B00005MDZY", "B00005BZE0", "B00008URUF", "B0000A9Y11", "B00005B8G1", "B00006FWTW", "B0001ZZNME", "B00005B8G3", "B000087PM3", "B0002TB4CW", "B00006LELB", "B00005J8EH", "B01EAG0VCG", "B000087H7T", "B0001ZZNLK", "B00002ST28", "B00005MO5G", "B00005LOW5", "B00000IYEQ", "B00000J9J9", "B00002SVEO", "B000084314", "B004910A8I", "B000QJ1NS8", "B01CL4RGXQ", "B01LXBW3KZ", "B000238EJ4", "B000084313", "B00005V9NJ", "B00005B8G2", "B000047GEI", "B079P7FKT6", "B00027NWRY", "B0002Y67PQ", "B0006GBCZU", "B076R5MMC6", "B01JOGH7SI", "B000GQ1G2E", "B00002ST27", "B0007D4MVI", "B01JYYWL7C", "B000B5MV6A", "B000070IW6", "B00005NECC", "B00008J2UZ", "B0000A09EP", "B000B5MV60", "B00000IYER", "B00002ST3U", "B0002Y67QA", "B000R08L7M", "B00023JJUW", "B00007CWJ0", "B072FRQZ65", "B000EGDEJY", "B000090W86", "B00AYBVB44", "B000A2R54M", "B0000A09EH", "B0019R361I", "B00002SVES", "B0000296ZM", "B000065SQ9", "B000035XB0", "B000Z8UMUK", "B00820R20Q", "B0002Y67PG", "B0006B0O9U", "B00000J97G", "B000A3I9YQ", "B00008DHNU", "B00006IJJI", "B000ERVMI8", "B00003OTI3", "B00005NCCW", "B00009WAUM", "B00005NCCA", "B00004SVW4", "B00008KUA3", "B00030GS80", "B0009Z3MOW", "B0001JXACA", "B0002GTXJG", "B000FO4KO8", "B00002STI2", "B000I10PY2", "B00002SVFZ", "B06XGWGZJ3", "B000ANYFW6", "B00005MI42"], "tech2": "", "brand": "Nintendo", "feature": ["Use Samus' energy blaster, missile launcher, bombs and balling-up ability to infiltrates a dangerous planet", "Collect power items and health tanks as you shoot your way through alien monsters and space pirates, while searching for the deadly Mother Brain"], "rank": [">#16,321 in Video Games (See Top 100 in Video Games)", ">#101 in Video Games > More Systems > Game Boy Advance > Games"], "also_view": ["B00009WAUO", "B00005UK88", "B00005B8FZ", "B00005MDZY", "B079P7FKT6", "B0001ZZNME", "B00000J9J9", "B00005BZE0", "B00008URUF", "B00006FWTW", "B00002ST28", "B0000A09EP", "B00006LELB", "B076R5MMC6", "B0009RF7VG", "B0002TB4CW", "B000YQ32TG", "B00004SVV7", "B00027NWRY", "B00005B8G1", "B0000A9Y11", "B000087PM3", "B000070IW6", "B000R08L7M", "B00002SVEO", "B00030GS80", "B00005B8G3", "B0019R361I", "B0001ZZNLK", "B0002Y67QA", "B000087H7T", "B000TUZCQI", "B000A2GX2W", "B000035XB0", "B00002SVES", "B01JYYWL7C", "B000047GEI", "B0006GBCZU", "B000084313", "B00005B8G2", "B0001JXACA", "B0001D0A2E", "B000B5MV60", "B000B5MV6A", "B00023JJUW", "B00004S9A0", "B000238EJ4", "B0002Y67Q0", "B00002ST3U", "B00005V9NJ", "B000QDG75I", "B0001ZZNM4", "B0006B0O9U", "B00008J2UZ", "B000A3I9YQ", "B00000J97G", "B000QJ1NS8", "B0007D4MVI"], "details": {}, "main_cat": "Video Games", "similar_item": "", "date": "", "price": "$162.25", "asin": "B0001ZZNNI", "imageURL": [], "imageURLHighRes": []}
    
3. Ratings
    商品ID,使用者ID,每一行的互動(評分),時間標記
    :::spoiler 範例
    0449819906,A3U4E9PIZ8OWH1,5.0,1383696000
    0449819906,A3945D2TJ0PI86,5.0,1488240000
    0449819906,A2WZK72HLQ7SPT,5.0,1487980800
    0449819906,A1Q7YJ1NPE6E0W,5.0,1485302400
    0449819906,A2846L8Q507JC4,5.0,1484179200

:::spoiler Code
```python!
if __name__ == '__main__':
args = parse_args()

# load interactions from raw rating file
# list of (user_ID, item_ID, rating, timestamp)
rating_inters = preprocess_rating(args)

# load item text from raw meta data file
# ex. ['0804161380', 'Legend of Zelda Box Set Prima Official Game Guide. . DIAMOND SELECT TOYS. ']
item_text_list = preprocess_text(args, rating_inters)

# split train([:-2])/valid(1)/test(1)
# ex(train). 50602: ['274', '201', '330']
train_inters, valid_inters, test_inters, user2index, item2index = \
    generate_training_data(args, rating_inters)

# device & plm initialization
device = set_device(args.gpu_id)
args.device = device
plm_tokenizer, plm_model = load_plm(args.plm_name)
plm_model = plm_model.to(device)

# create output dir
check_path(os.path.join(args.output_path, args.dataset))

# generate PLM emb and save to file
# input: item_text_list, item2index
# Output embeddings shape:  (16875, 768)
generate_item_embedding(args, item_text_list, item2index, 
                        plm_tokenizer, plm_model, word_drop_ratio=-1)
# pre-stored word drop PLM embs
# (not used here)
if args.word_drop_ratio > 0:
    generate_item_embedding(args, item_text_list, item2index, 
                            plm_tokenizer, plm_model, word_drop_ratio=args.word_drop_ratio)

# save interaction sequences into atomic files
convert_to_atomic_files(args, train_inters, valid_inters, test_inters)

# save useful data
write_text_file(item_text_list, os.path.join(args.output_path, args.dataset, f'{args.dataset}.text'))
write_remap_index(user2index, os.path.join(args.output_path, args.dataset, f'{args.dataset}.user2index'))
write_remap_index(item2index, os.path.join(args.output_path, args.dataset, f'{args.dataset}.item2index'))
```
:::
    
### 流程    
1. 讀取使用者互動資料(preprocess_rating)
    用途:讀取互動資料，並進行篩選(使用K-core filtering&互動資訊沒有metadata)
    
    輸出格式:(user_ID, item_ID, rating, timestamp)
2. 讀取商品資料(preprocess_text)
    用途:讀取商品資料 **(只取 ID,名稱，類別，品牌)**
    
    範例:['0804161380', 'Legend of Zelda Box Set Prima Official Game Guide. . DIAMOND SELECT TOYS. ']
3. 產生訓練/驗證/測試 資料(generate_training_data)
    用途:產生三種資料，並將使用者與商品以數字的方式表達
    另外，使用了leave one out的方法，取最後一個為測試，前一個為驗證，剩餘為訓練(split train([:-2])/valid(1)/test(1))
    
    範例. (train). 50602: ['274', '201', '330']

4.讀取模型
    用途:讀取模型+GPU
    (這個實作使用 **bert-base-uncased**)
    
5.產生商品的embedding(generate_item_embedding)
    用途:使用之前產生的item_text_list, item2index，產生表示每個物品的embedding
    
    輸入: item_text_list, item2index
    輸出:embeddings shape:  (16875, 768)
    (16875是總共的商品數目，768是經過Bert產生的維度)
6.產生微調輸入的資料(convert_to_atomic_files)
    用途:產生訓練，驗證，測試輸入資料
    產生方式
    a.訓練:在互動串列中，把最後一個當作目標商品，剩下為商品序列(最多從後取50個)，隨後刪減一個物品
:::spoiler 範例
    0	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15	16
    0	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14	15
    0	0 1 2 3 4 5 6 7 8 9 10 11 12 13	14
    0	0 1 2 3 4 5 6 7 8 9 10 11 12	13
    0	0 1 2 3 4 5 6 7 8 9 10 11	12
    0	0 1 2 3 4 5 6 7 8 9 10	11
    0	0 1 2 3 4 5 6 7 8 9	10
    0	0 1 2 3 4 5 6 7 8	9
    0	0 1 2 3 4 5 6 7	8
    0	0 1 2 3 4 5 6	7
    0	0 1 2 3 4 5	6
    0	0 1 2 3 4	5
    0	0 1 2 3	4
    0	0 1 2	3
    0	0 1	2
    0	0	1
:::
    
b.驗證:從訓練資料中拿取資料(從後取50個)，之後加入之前新增的驗證商品
:::spoiler 範例
0	0 1 2 3 4	5
1	7 8 9 10	11
2	13 14 15 16	17
3	19 20 21 22 23 24 25 26 27	28
4	30 31 32 33 34	35
5	37 38 39 40 41 42 43 44	45
6	47 48 49 50 51 52 53 54 55 56 57 58 59 60	61
7	63 64 65 66 67 68	69
8	71 72 73 74	75
9	77 78 79 80 81 82 83 84	85
10	87 88 89 90 91 92 93 94	23
:::
c.測試:從訓練+驗證資料中拿取資料(從後取50個)，之後加入之前新增的測試商品
    
:::spoiler 範例
0	0 1 2 3 4 5	6
1	7 8 9 10 11	12
2	13 14 15 16 17	18
3	19 20 21 22 23 24 25 26 27 28	29
4	30 31 32 33 34 35	36
5	37 38 39 40 41 42 43 44 45	46
6	47 48 49 50 51 52 53 54 55 56 57 58 59 60 61	62
7	63 64 65 66 67 68 69	70
8	71 72 73 74 75	76
9	77 78 79 80 81 82 83 84 85	86
10	87 88 89 90 91 92 93 94 23	95
:::
    
### 問題
1.finetune所使用的資料，要和pretrain的資料相似嗎?
2.產生的微調資料不相同