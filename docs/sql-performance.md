# SQLのクエリ最適化の記録

見出しh2にエンドポイント

## api/products

2021/4/4時点のテストデータ

```md
before
185queries in 190ms
after
default 103.52 ms (71 queries including 68 similar and 61 duplicates )
```

とりあえずProductSerialzierから半分程度N+1を解決できたはず。

さらに、product__reviewの先にあるreviewerについても、必要なときにSQLを発行させることで短縮できた。ダブったクエリは0になった。manyToManyのクエリは表面上変わりないが、バックエンドでうまいことcacheされるから、大丈夫なはず。データ大量投入後にチェックする。

```md
after
default 19.51 ms (6 queries )
```

## api/
