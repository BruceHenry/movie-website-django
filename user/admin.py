from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
# admin.site.unregister(User)

# class UserAdmin(admin.ModelAdmin):
#     # This will help you to disbale add functionality
#     def has_add_permission(self, request):
#         return False
# admin.site.register(User, UserAdmin)

# admin.site.register(Profile)

# admin.site.register(CommentToPost)
# admin.site.register(PostToUser)
# admin.site.register(Follow)
# admin.site.register(Activity)
# admin.site.register(Notification)
# admin.site.register(UserSeenNotifycation)

# from django.contrib import admin
# from django_with_extra_context_admin.admin import DjangoWithExtraContextAdmin
# from .models import *

# class ActivityAdmin(DjangoWithExtraContextAdmin, admin.ModelAdmin):

#     django_with_extra_context_admin_view_name = False

#     def get_extra_context(self, request, **kwargs):
#         extra_context = super().get_extra_context(request, **kwargs) or {}
#         extra_context.update({
#             "count_acivity": Activity.objects.all().count(),
#         })
#         return extra_context

# admin.site.register(Activity, ActivityAdmin)
