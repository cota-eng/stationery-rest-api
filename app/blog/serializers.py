from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from . import models 
class PostSerializer(ModelSerializer):
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
        comment_qs = models.Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(data=comment_qs, many=True).data
        return comments

def create_comment_serializer(type="post", slug=None, parent_id=None):
    class CommentCreateSeralizer(ModelSerializer):
        class Meta:
            model = models.Comment
            fields = (
                'id',
                'parent',
                'content',
            )

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = models.Comment
        fields = "__all__"
    def get_reply_count(self, obj)->int:
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
    
class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    class Meta:
        model = models.Comment
        fields = "__all__"
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None