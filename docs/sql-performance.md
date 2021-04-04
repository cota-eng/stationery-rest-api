# SQLのクエリ最適化の記録

## api/products

2021/4/4時点のテストデータ

```md
before
185queries in 190ms
after
default 103.52 ms (71 queries including 68 similar and 61 duplicates )
```

とりあえずProductSerialzierから半分程度N+1を解決できたはず。
