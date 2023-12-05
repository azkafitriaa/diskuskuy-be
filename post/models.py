from django.db import models
from tinymce.models import HTMLField 
from django.contrib.auth.models import User
from forum.models import Thread
from autentikasi.models import CustomUser
from django.shortcuts import get_object_or_404

class Post(models.Model):
    tag = models.CharField(max_length=100, default="pertanyaan")
    content = HTMLField(default="")
    date = models.DateTimeField(auto_now=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="post")
    likes = models.ManyToManyField(User, default=None, blank=True, related_name="likes")
    claps = models.ManyToManyField(User, default=None, blank=True, related_name="claps")
    loves = models.ManyToManyField(User, default=None, blank=True, related_name="loves")

    def __str__(self):
        return self.content

    @property
    def creator_name(self):
        custom_user = get_object_or_404(CustomUser.objects.all(), user=self.creator)
        return custom_user.name
    
    @property
    def creator_photo_url(self):
        custom_user = get_object_or_404(CustomUser.objects.all(), user=self.creator)
        if custom_user.photo_url:
            return custom_user.photo_url
        return None
    
    @property
    def creator_role(self):
        custom_user = get_object_or_404(CustomUser.objects.all(), user=self.creator)
        return custom_user.role
    
    @property
    def creator_group(self):
        custom_user = get_object_or_404(CustomUser.objects.all(), user=self.creator)
        return custom_user.group.name
    
    @property
    def number_of_likes(self):
        return self.likes.count()
    
    @property
    def number_of_claps(self):
        return self.claps.count()
    
    @property
    def number_of_loves(self):
        return self.loves.count()

class InitialPost(models.Model):
    seen = models.ManyToManyField(User, default=None, blank=True, related_name="seen")
    thread = models.OneToOneField(Thread, on_delete=models.CASCADE, default=None, related_name="initial_post")
    post = models.OneToOneField(Post, on_delete=models.CASCADE, default=None, related_name="initial_post")

    @property
    def seen_user_info(self):
        return [CustomUser.objects.get(user=user) for user in self.seen.all()]

class ReplyPost(models.Model):
    initial_post = models.ForeignKey(InitialPost, on_delete=models.CASCADE, default=None, related_name="reply_post")
    post = models.OneToOneField(Post, on_delete=models.CASCADE, default=None, related_name="reply_post")

class NestedReplyPost(models.Model):
    reply_post = models.ForeignKey(ReplyPost, on_delete=models.CASCADE, default=None, related_name="nested_reply_post")
    post = models.OneToOneField(Post, on_delete=models.CASCADE, default=None, related_name="nested_reply_post")

