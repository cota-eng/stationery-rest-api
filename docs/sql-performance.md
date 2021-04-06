# SQL のクエリ最適化の記録

見出し h2 にエンドポイント

## api/products

2021/4/4 時点のテストデータ

```md
before
185queries in 190ms
after
default 103.52 ms (71 queries including 68 similar and 61 duplicates )
```

とりあえず ProductSerialzier から半分程度 N+1 を解決できたはず。

さらに、product\_\_review の先にある reviewer についても、必要なときに SQL を発行させることで短縮できた。ダブったクエリは 0 になった。manyToMany のクエリは表面上変わりないが、バックエンドでうまいこと cache されるから、大丈夫なはず。データ大量投入後にチェックする。

```md
after
default 19.51 ms (6 queries )
```

## api/fav-list

```md
before
default 11.13 ms (5 queries including 3 similar )
after
default 11.53 ms (3 queries )
```

## api/tag

```md
before
default 19.96 ms (15 queries including 13 similar )
after
default 9.83 ms (3 queries )
```

## api/user

```md
default 23.77 ms (22 queries including 20 similar and 10 duplicates )
=>
default 11.56 ms (11 queries including 10 similar and 10 duplicates )
=>
default 3.50 ms (1 query )
```

## api/profile

```md
default 5.54 ms (3 queries )
=>
default 4.01 ms (2 queries )
```

## api/allprofile

```md
default 79.65 ms (48 queries including 47 similar and 18 duplicates )
=>
default 41.29 ms (28 queries including 26 similar )
=>
default 20.18 ms (14 queries including 10 similar )
=>
```

## api/category

```md
default 6.78 ms (5 queries including 3 similar )
=>
default 7.55 ms (3 queries )
```

## api/brand

```md
default 15.22 ms (12 queries including 10 similar )
=>
default 7.45 ms (3 queries )
```

## api/

```md

```

## api/

```md

```
