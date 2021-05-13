from django.contrib import admin
from user.models import *
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(CommentToPost)
admin.site.register(PostToUser)
admin.site.register(Follow)
admin.site.register(Activity)
