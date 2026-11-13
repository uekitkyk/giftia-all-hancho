-- 001_create_tables.sql — 思い出しガイド付き検索の追加テーブル（要件定義書 5.2）

CREATE TABLE questions (
  question_id   INT  NOT NULL,
  question_text TEXT NOT NULL,
  display_order INT  NOT NULL,
  PRIMARY KEY (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs;

CREATE TABLE choices (
  choice_id   INT          NOT NULL,
  question_id INT          NOT NULL,
  choice_text VARCHAR(255) NOT NULL,
  PRIMARY KEY (choice_id),
  FOREIGN KEY (question_id) REFERENCES questions(question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs;

CREATE TABLE choice_life_tags (
  choice_id INT         NOT NULL,
  life_tag  VARCHAR(20) NOT NULL,
  PRIMARY KEY (choice_id, life_tag),
  FOREIGN KEY (choice_id) REFERENCES choices(choice_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs;

CREATE TABLE product_life_tags (
  product_id VARCHAR(10) NOT NULL,
  life_tag   VARCHAR(20) NOT NULL,
  PRIMARY KEY (product_id, life_tag),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs;