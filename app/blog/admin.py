from django.contrib import admin

from .models import Post,Comment

# class PostModelAdmin(admin.ModelAdmin):
#     list_display = ["titie", "updated_at"]
#     list_display_links = ["updated_at"]
#     list_editable = ["title"]
#     list_filter = ["updated_at"]
#     search_fields = ["title", "content"]
    
#     class Meta:
#         model = Post
        
admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(Post,PostModelAdmin)