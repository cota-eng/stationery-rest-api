from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from . import models 
from rest_framework.exceptions import  ValidationError

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
from django.contrib.contenttypes.models import ContentType

def create_comment_serializer(model_type="post", slug=None, parent_id=None):
    
    class CommentCreateSeralizer(ModelSerializer):
        class Meta:
            model = models.Comment
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
                parent_qs = models.Comment.filter(id=parent_id)
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

    return CommentCreateSeralizer

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