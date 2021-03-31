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

    def get_markdown(self, obj):
        return obj.get_markdown()

class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


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