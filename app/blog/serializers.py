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
    pass