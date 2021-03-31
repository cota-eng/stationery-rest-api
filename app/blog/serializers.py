from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from .models import Post,Comment
from rest_framework.exceptions import  ValidationError
from django.contrib.auth import get_user_model

class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "is_public",
            "author",
            "created_at",
            "updated_at",
        )


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "is_public",
            "author",
            "created_at",
            "updated_at",
        )

    url = HyperlinkedIdentityField(
        view_name="",
        lookup_field="",
    )
    markdown = SerializerMethodField()
    comments = SerializerMethodField()

    def get_markdown(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comment_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(data=comment_qs, many=True).data
        return comments

from django.contrib.contenttypes.models import ContentType

def create_comment_serializer(model_type="post", slug=None, parent_id=None,user=None):

    class CommentCreateSeralizer(ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                'id',
                'parent',
                'content',
            )
        
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_id = parent_qs.first()

            return super(CommentCreateSeralizer, self).__init__(*args, **kwargs)
        
        def validate(self, attrs):
            model_type = self.model_type
            model_qs = ContentType.object.filter(model=model_type)
            if not model_qs.exists() or model_qs.count > 1:
                raise ValidationError("error")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("error")
            return attrs

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = get_user_model().objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type,
                slug,
                content,
                main_user,
                parent_obj=parent_obj,
            )
            return comment

    return CommentCreateSeralizer

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"
    def get_reply_count(self, obj)->int:
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    
class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None