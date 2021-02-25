# 文房具のレビューサイト用のRESTAPI

Djangoで作っているRESTに則ったAPIです。

フロントエンドと疎結合化し、開発を楽にしています。

## 課題と実装予定

- データのスクレイピング
- 写真のクラウドへの保存
- アバター画像の選択
- 関連ペンの提示（カテゴリ・タグから判断）
- お気に入りに追加する機能（API未完成）
- OGP

## 使用技術・環境
- Python
- Django(RestFramework)
- Docker(python3.8-slim)
- PostgreSQL
- pip(requirements.txt)

## 実際の様子
未デプロイのためスクリーンショット

- ペン一覧

![2021-02-24_08h40_00](https://user-images.githubusercontent.com/65804288/108993212-97b4f180-76dd-11eb-9201-b3cc3224e759.png)

- 条件検索

![2021-02-24_08h40_36](https://user-images.githubusercontent.com/65804288/108993195-9388d400-76dd-11eb-8221-4fd2305a7182.png)

- 自身のプロフィールのCRUD（未認証）

![2021-02-24_08h38_35](https://user-images.githubusercontent.com/65804288/108993199-94ba0100-76dd-11eb-855b-6fa5e11bc646.png)

- 自身のプロフィールのCRUD（認証済）

![2021-02-24_08h39_25](https://user-images.githubusercontent.com/65804288/108993204-95eb2e00-76dd-11eb-966c-a8fe33d1a822.png)
