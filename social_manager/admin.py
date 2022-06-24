from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(UserPosts)
admin.site.register(PostComments)
admin.site.register(Follow)
admin.site.register(PostSave)
admin.site.register(Notification)
