from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile
from .models import Message
from .models import Topic
from .models import Topiccomment
from .models import News
from .models import NewsComment
from .models import Photo
from .models import PhotoComment


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message


admin.site.register(Message, MessageAdmin)

admin.site.register(Topic)

admin.site.register(Topiccomment)

admin.site.register(News)

admin.site.register(NewsComment)

admin.site.register(Photo)

admin.site.register(PhotoComment)

