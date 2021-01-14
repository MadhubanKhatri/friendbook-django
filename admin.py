from django.contrib import admin
from .models import User, Post, Comment, Follower
# Register your models here.
@admin.register(User)
class userAdmin(admin.ModelAdmin):
  list_display = ('id', 'full_name', 'user_name', 'email', 'password')

@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'post', 'comment')


admin.site.register(Post)

admin.site.register(Follower)
