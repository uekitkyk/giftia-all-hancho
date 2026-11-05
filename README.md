Giftia
Tech0 13期「オールはんちょー」の共同開発プロジェクト。

1. プロジェクト概要
   フロントエンド：Next.js（giftia-frontend/）
   バックエンド：FastAPI（backend/）
   ソースコードはGitHubで共有し、GitHub Flowに沿って共同開発する。

2. 開発の基本ルール
   mainブランチを直接編集しない。
   作業を始める前にmainをpullして最新化する。
   作業ごとにfeatureブランチを作成する。
   変更が終わったらPull Request（PR）を作成する。
   PRは本人以外の班員が確認し、Approveする。
   Approve後にmainへmergeする。
   merge後は全員がmainをpullする。

3. ブランチの命名ルール
   feature/作業内容 の形式とする。
   例：feature/create-agents-md
   ブランチ名は英数字とハイフンを基本とする。

4. PR・レビューのルール
   PRには次の3点を記載する。
   何を変更したか
   なぜ変更したか
   どうやって確認するか
   レビュー担当者は、変更内容と関係ないファイルが含まれていないか確認する。

5. 情報管理
   .envなどの秘密情報をGitHubにpushしない。
   APIキーやパスワードをソースコードに記載しない。
   不明点やエラーは班員間で共有する。

6. AI活用ルール
   AIの利用に関する詳細は、AGENTS.mdを参照する。
