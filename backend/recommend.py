"""思い出しガイドの質問と、商品推薦（Phase1）

いまの版（B1）：DB を使わず、下のダミーデータで動く。
    うえっきーさん担当のフロントが土日に画面をつなげるように、本物と同じ形の JSON を先に返す。
次の版（B2）：get_questions() と recommend() の中身を、DB への SQL に置き換える。
    使うテーブル：questions / choices / choice_life_tags / product_life_tags / products
    関数の名前と、返す形は変えない（main.py と画面を直さずに済むように）。

順位のルール（要件定義書 FR-01・6.2）
    スコア　＝ 回答から出てきた生活場面タグと、商品のタグが一致した「種類の数」
              （別の選択肢が同じタグを指しても1回と数える）
    候補　　＝ 生活場面タグを持つ商品のうち、在庫があり（stock > 0）、スコアが1以上のもの
    並び順　＝ スコアの高い順 → 評価（rating）の高い順 → レビュー数の多い順 → 商品IDの昇順
              販売数（sales_count）は使わない（BR-03「ランキング外でも」と矛盾するため）
"""

# ダミーデータ（B2で置き換える）
# 選択肢IDは「質問の番号×100＋何番目か」。tagはその選択肢に対する生活場面タグ（choice_life_tagsに当たる）
DUMMY_QUESTIONS = [
    {
        "id": 1,
        "order": 1,
        "text": "お母さんの毎日の習慣は？",
        "choices": [
            {"id": 101, "text": "朝にコーヒーや紅茶を飲む", "tags": ["お茶の時間"]},
            {"id": 102, "text": "毎日料理をする", "tags": ["料理"]},
            {"id": 103, "text": "散歩や体操をする", "tags": ["健康づくり"]},
        ],
    },
    {
        "id": 2,
        "order": 2,
        "text": "お母さんは休みの日はどう過ごしていますか？",
        "choices": [
            {"id": 201, "text": "庭やベランダで植物を育てる", "tags": ["園芸"]},
            {"id": 202, "text": "本や雑誌を読む", "tags": ["読書"]},
            {"id": 203, "text": "家でゆっくり過ごす", "tags": ["リラックス"]},
        ],
    },
    {
        "id": 3,
        "order": 3,
        "text": "最近「便利そうね」と言っていた物は？",
        "choices": [
            {"id": 301, "text": "キッチンの小さな家電", "tags": ["料理", "時短"]},
            {"id": 302, "text": "手入れが楽な日用品", "tags": ["時短"]},
            {"id": 303, "text": "特に思い当たらない", "tags": []},
        ],
    },
    {
        "id": 4,
        "order": 4,
        "text": "最近、困っていそうなことは？",
        "choices": [
            {"id": 401, "text": "手や肌の乾燥", "tags": ["肌のケア"]},
            {"id": 402, "text": "寝つきが悪い", "tags": ["睡眠"]},
            {"id": 403, "text": "体重が増えている", "tags": ["健康", "ダイエット"]},
        ],
    },
    {
        "id": 5,
        "order": 5,
        "text": "一緒に過ごすとき、何をすることが多いですか？",
        "choices": [
            {"id": 501, "text": "お茶を飲みながら話す", "tags": ["お茶の時間"]},
            {"id": 502, "text": "一緒に料理をする", "tags": ["料理"]},
            {"id": 503, "text": "旅行や外出をする", "tags": ["旅行", "お出かけ"]},
        ],
    },
]

# 商品名はDBの列名のまま持つ（B2でSQLの結果に差し替えてもmain.pyのto_giftがそのまま使える）
# IDは本物と見分けられるように「D」で始める
DUMMY_PRODUCTS = [
    {
        "product_id": "D001",
        "product_name": "【ダミー】小型電気ケトル0.8L",
        "category": "キッチン家電",
        "brand": "ダミー電機",
        "price": 4980,
        "rating": 4.3,
        "review_count": 120,
        "stock": 10,
        "tags": ["料理", "時短", "お茶の時間"],
    },
    {
        "product_id": "D002",
        "product_name": "【ダミー】日本茶 飲み比べセット",
        "category": "食品・飲料",
        "brand": "ダミー茶園",
        "price": 3240,
        "rating": 4.5,
        "review_count": 80,
        "stock": 25,
        "tags": ["お茶の時間"],
    },
    {
        "product_id": "D003",
        "product_name": "【ダミー】有田焼 湯呑みペア",
        "category": "食器",
        "brand": "ダミー窯",
        "price": 3960,
        "rating": 4.5,
        "review_count": 80,
        "stock": 8,
        "tags": ["お茶の時間"],
    },
    {
        "product_id": "D004",
        "product_name": "【ダミー】ガーデニング手袋とハサミのセット",
        "category": "ガーデニング",
        "brand": "ダミーガーデン",
        "price": 3850,
        "rating": 4.1,
        "review_count": 35,
        "stock": 12,
        "tags": ["園芸"],
    },
    {
        "product_id": "D005",
        "product_name": "【ダミー】本革ブックカバー",
        "category": "雑貨",
        "brand": "ダミーレザー",
        "price": 4400,
        "rating": 4.4,
        "review_count": 52,
        "stock": 6,
        "tags": ["読書"],
    },
    {
        "product_id": "D006",
        "product_name": "【ダミー】ハンドクリーム 3本セット",
        "category": "コスメ",
        "brand": "ダミーコスメ",
        "price": 2970,
        "rating": 4.2,
        "review_count": 210,
        "stock": 30,
        "tags": ["肌のケア"],
    },
    {
        "product_id": "D007",
        "product_name": "【ダミー】軽くて切れる三徳包丁",
        "category": "キッチン用品",
        "brand": "ダミー刃物",
        "price": 5500,
        "rating": 4.6,
        "review_count": 95,
        "stock": 4,
        "tags": ["料理", "時短"],
    },
    {
        "product_id": "D008",
        "product_name": "【ダミー】電動ごまミル（在庫切れ）",
        "category": "キッチン家電",
        "brand": "ダミー電機",
        "price": 3300,
        "rating": 4.8,
        "review_count": 60,
        "stock": 0,
        "tags": ["料理"],
    },
]


def get_questions() -> list[dict]:
    """質問と選択肢を表示順に返す（画面に渡す形。tagsは画面に見せないので外す）"""
    return [
        {
            "id": q["id"],
            "order": q["order"],
            "text": q["text"],
            "choices": [{"id": c["id"], "text": c["text"]} for c in q["choices"]],
        }
        for q in sorted(DUMMY_QUESTIONS, key=lambda q: q["order"])
    ]


def recommend(choice_Ids: list[int]) -> list[dict]:
    """選ばれた選択肢IDから、推薦する商品を順位通りに返す。返す行はDBの列名（product_idなど）に、scoreとmatched_tagsを足したもの"""
    # 　①選択肢ID　→　生活場面タグ（重複は1つにまとめて回答した順番はたもつ）。知らないIDは無視する。
    tag_of_choice = {c["id"]: c["tags"] for q in DUMMY_QUESTIONS for c in q["choices"]}
    answer_tags: list[str] = []
    for cid in choice_Ids:
        for tag in tag_of_choice.get(cid, []):
            if tag not in answer_tags:
                answer_tags.append(tag)

    # ②在庫がある商品ごとに一致したタグの種類の数をスコアにする。0点の商品は候補にしない。
    rows = []
    for p in DUMMY_PRODUCTS:
        if p["stock"] <= 0:
            continue
        matched = [t for t in answer_tags if t in p["tags"]]
        if matched:
            rows.append({**p, "score": len(matched), "matched_tags": matched})

    # ③スコアの高い順 → 評価（rating）の高い順 → レビュー数の多い順 → 商品IDの順番に並べる
    rows.sort(
        key=lambda r: (-r["score"], -r["rating"], -r["review_count"], r["product_id"])
    )
    return rows
