from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .models import *

class PostSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField()
    creator_photo_url = serializers.ReadOnlyField()
    creator_role = serializers.ReadOnlyField()
    creator_group = serializers.ReadOnlyField()
    number_of_likes = serializers.ReadOnlyField()
    number_of_claps = serializers.ReadOnlyField()
    number_of_loves = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'

class PostWeekSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField()
    creator_photo_url = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('creator_name', 'creator_photo_url')

class NestedReplyPostSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = NestedReplyPost
        fields = '__all__'

    def create(self, validated_data):
        reply_post = get_object_or_404(ReplyPost.objects.all(), pk=validated_data['reply_post'].id)
        post_data = validated_data['post']
        post = Post(
            tag=post_data['tag'],
            content=post_data['content'],
            creator=post_data['creator'],
        )
        post.save()
        nested_reply_post = NestedReplyPost(
            post=post,
            reply_post=reply_post
        )
        nested_reply_post.save()
        return nested_reply_post
    
    def update(self, instance, validated_data):
        if 'post' in validated_data:
            post_data = validated_data.pop('post')
            post = instance.post
            post.tag = post_data.get('tag', post.tag)
            post.content = post_data.get('content', post.content)
            post.save()
            return instance
        return Response(status=status.HTTP_400_BAD_REQUEST) 

# class NestedReplyPostResponseSerializer(serializers.ModelSerializer):
#     post = PostSerializer(read_only=True)

#     class Meta:
#         model = NestedReplyPost
#         fields = ('id', 'post')        

class ReplyPostSerializer(serializers.ModelSerializer):
    nested_reply_post = NestedReplyPostSerializer(read_only=True, many=True)
    post = PostSerializer()

    class Meta:
        model = ReplyPost
        fields = '__all__'
        extra_kwargs = {'initial_post': {'write_only': True}}

    def create(self, validated_data):
        initial_post = get_object_or_404(InitialPost.objects.all(), pk=validated_data['initial_post'].id)
        post_data = validated_data['post']
        post = Post(
            tag=post_data['tag'],
            content=post_data['content'],
            creator=post_data['creator'],
        )
        post.save()
        reply_post = ReplyPost(
            post=post,
            initial_post=initial_post
        )
        reply_post.save()
        return reply_post
    
    def update(self, instance, validated_data):
        if 'post' in validated_data:
            post_data = validated_data.pop('post')
            post = instance.post
            post.tag = post_data.get('tag', post.tag)
            post.content = post_data.get('content', post.content)
            post.save()
            return instance
        return Response(status=status.HTTP_400_BAD_REQUEST) 

# class ReplyPostResponseSerializer(serializers.ModelSerializer):
#     post = PostSerializer(read_only=True)

#     class Meta:
#         model = ReplyPost
#         fields = ('id', 'post')

class InitialPostSerializer(serializers.ModelSerializer):
    reply_post = ReplyPostSerializer(read_only=True, many=True)
    post = PostSerializer()

    class Meta:
        model = InitialPost
        fields = '__all__'
        extra_kwargs = {'thread': {'write_only': True}}

class InitialPostWeekThreadSerializer(serializers.ModelSerializer):
    post = PostWeekSerializer(read_only=True)

    class Meta:
        model = InitialPost
        fields = ['post']

class InitialPostSeenSerializer(serializers.Serializer):
    seen = serializers.ListField()