-- 002b_update_q4.sql — 古い 002（Q4＝家事・タグ「家事ラク」）をすでに実行したDBを、今の 002 に合わせる
-- 商品データに「家事ラク」に当たる商品がないため、Q4 を「最近の楽しみ」、タグを「お出かけ好き」に替えた。
-- 新しく作るDBでは不要（001 → 002 → 003 の順に実行すれば、最初から新しい内容になる）。

START TRANSACTION;

UPDATE questions SET question_text = 'お母さんの最近の楽しみは？' WHERE question_id = 4;

UPDATE choices SET choice_text = '友だちと出かける・旅行' WHERE choice_id = 401;
UPDATE choices SET choice_text = '料理をする'             WHERE choice_id = 402;
UPDATE choices SET choice_text = '特にない'               WHERE choice_id = 403;

UPDATE choice_life_tags SET life_tag = 'お出かけ好き' WHERE choice_id = 401 AND life_tag = '家事ラク';

COMMIT;
