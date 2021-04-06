# ContentTypeまとめる

contenttypeの取り出し方

hoge_type = ContentType.objects.get(app_label="",model="")
or
.objects.get_for_model("")
>>> ContentType.objects.get_for_model(User)
<ContentType: authentication | ユーザー>
規模が大きいとModelNameかぶりうる。前者を使うと気にすることないからベター？

```python
>>> usertype = ContentType.objects.get(app_label="authentication",model="user")
>>> usertype
<ContentType: authentication | ユーザー>
あくまでタイプを持ってきただけなので、
これでModelをとるには、以下のメソッド
model = usertype.model_class()
>>> model = usertype.model_class()
>>> model
<class 'authentication.models.User'>
となる。

>>> model.objects.all()
<QuerySet [<User: userb>, <User: userc>, <User: d>, <User: e>, <User: f>, <User: admin>]>
実際にもってこれる

ユーザーモデルの特定のユーザーをgetするには
>>> usertype.get_object_for_this_type(username="admin")   
<User: admin>



Comment.objects.create(content_object=post,comment_by_id="01F2K0QVTSBZ1K0JZXS7ASYFHA",post_id=1)
```

固定

```python
これでAppとModel指定できる、どっちでもいい
limit = models.Q(app_label='', model='') | \
        models.Q(app_label='', model='')

content_type = models.ForeignKey(
    ContentType,
    verbose_name=_(''),
    limit_choices_to=limit,
    # かならずNULL　OK
    null=True,
    blank=True,
)

object_id = models.PositiveIntegerField(
    verbose_name=_('related object'),
    null=True,
)
UUID,ULIDを使っている場合はCharFieldに置き換えるはず

content_object = generic.GenericForeignKey('content_type', 'object_id')
```

Adminのカスタム

```python
class PollAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'question'
                # ...
            )
        }),
        (_('page/article'), {
            'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id', )
        }),
    )
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }

```