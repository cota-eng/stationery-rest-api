# user apiについて

特定のユーザーのページがあり、そこで見られるものは

- ニックネーム
- Twitterアカウント
- review一覧
- 後々、筆箱一覧

エンドポイントは api/user/[user_id]
profile_idのつかいどころが混在している、、、

ReviewにはUserモデルが紐付いている
Profileモデルにはユーザーの一対一、アバターが紐付いている
