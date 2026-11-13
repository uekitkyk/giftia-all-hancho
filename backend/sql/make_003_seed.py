# make_003_seed.py — 確認用CSV（003_product_life_tags_review.csv）から 003_seed_product_life_tags.sql を作る
# 使い方（backend/sql で）：python make_003_seed.py
#   CSV の「確認」列が NG の行は入れない。「修正後タグ」列に書いたら、そちらを使う（「・」区切り）。

import csv
from pathlib import Path

HERE = Path(__file__).parent
CSV_PATH = HERE / "003_product_life_tags_review.csv"
SQL_PATH = HERE / "003_seed_product_life_tags.sql"

# 002_seed_questions.sql の choice_life_tags と同じ表記だけを使う
LIFE_TAGS = ["お茶時間", "コーヒー時間", "晩酌", "甘いもの好き", "料理好き", "ガーデニング", "花のある暮らし",
             "手肌ケア", "リラックス", "健康志向", "冷え対策", "お出かけ好き"]

pairs, skipped = [], []
with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        if row["確認"].strip().upper() == "NG":
            skipped.append(row["product_id"])
            continue
        tags = (row["修正後タグ"].strip() or row["生活場面タグ案"]).split("・")
        for tag in (t.strip() for t in tags if t.strip()):
            if tag not in LIFE_TAGS:
                raise SystemExit(f"{row['product_id']}: 一覧にないタグ「{tag}」（表記ゆれに注意）")
            pairs.append((row["product_id"], tag))

lines = [
    "-- 003_seed_product_life_tags.sql — 初期100商品の生活場面タグ（要件定義書 5.2 / 5.4）",
    "-- make_003_seed.py で 003_product_life_tags_review.csv から自動生成。直接は編集せず、CSV を直して作り直す。",
    "-- 先に 001・002 を実行しておく。",
    "",
    "START TRANSACTION;",
    "",
    "DELETE FROM product_life_tags;  -- 作り直すたびに入れ直す",
    "",
    "INSERT INTO product_life_tags (product_id, life_tag) VALUES",
    ",\n".join(f"  ('{pid}', '{tag}')" for pid, tag in pairs) + ";",
    "",
    "COMMIT;",
    "",
]
SQL_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"{len({p for p, _ in pairs})} 商品・{len(pairs)} 行を書き出しました（NG で除外：{len(skipped)} 件）")
