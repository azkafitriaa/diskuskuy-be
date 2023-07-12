from rest_framework import serializers
from .models import *
from post.serializers import *
from django.shortcuts import get_object_or_404
from datetime import datetime

class ReferenceFileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFile
        fields = '__all__'

class ReferenceFileThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFile
        fields = ('id','title', 'url')

# class SummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Summary
#         fields = '__all__'

# class SummaryThreadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Summary
#         fields = ('id','content')

# class DiscussionGuideRequestSerializer(serializers.ModelSerializer):
#     thread_title = serializers.ReadOnlyField()
#     week_name = serializers.ReadOnlyField()

#     class Meta:
#         model = DiscussionGuide
#         fields = '__all__'

# class DiscussionGuideStateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiscussionGuide
#         fields = ('id','state')

# class DiscussionGuideThreadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiscussionGuide
#         fields = ('id','deadline','description','mechanism_expectation', 'state')
#         read_only_fields = ['state']

# class DiscussionGuideWeekThreadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiscussionGuide
#         fields = ['deadline']

class ThreadRequestSerializer(serializers.ModelSerializer):
    initial_post = InitialPostSerializer()
    reference_file = ReferenceFileThreadSerializer(many=True)
    # summary = SummaryThreadSerializer(read_only=True)
    # discussion_guide = DiscussionGuideThreadSerializer()
    week_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Thread
        fields = '__all__'
    
    def create(self, validated_data):
        week = get_object_or_404(Week.objects.all(), pk=validated_data['week'].id)
        thread = Thread(
            title=validated_data['title'],
            deadline=validated_data['deadline'],
            description=validated_data['description'],
            mechanism_expectation=validated_data['mechanism_expectation'],
            week=week
        )
        thread.save()
        initial_post_data = validated_data['initial_post']
        post_data = initial_post_data['post']
        post = Post(
            tag=post_data['tag'],
            content=post_data['content'],
            creator=post_data['creator'],
        )
        post.save()
        initial_post = InitialPost(
            post=post,
            thread=thread
        )
        initial_post.save()
        # discussion_guide_data = validated_data['discussion_guide']
        # discussion_guide=DiscussionGuide(
        #     deadline=discussion_guide_data['deadline'],
        #     description=discussion_guide_data['description'],
        #     mechanism_expectation=discussion_guide_data['mechanism_expectation'],
        #     thread=thread
        # )
        # discussion_guide.save()
        reference_file_datas = validated_data['reference_file']
        for reference_file_data in reference_file_datas:
            reference_file=ReferenceFile(
                title=reference_file_data['title'],
                url=reference_file_data['url'],
                thread=thread
            )
            reference_file.save()
        return thread

    def update(self, instance, validated_data):
        if 'initial_post' in validated_data:
            initial_post_data = validated_data.pop('initial_post')
            initial_post_post_data = initial_post_data.pop('post')
            initial_post = instance.initial_post
            initial_post_post = initial_post.post
            initial_post_post.tag = initial_post_post_data.get('tag', initial_post_post.tag)
            initial_post_post.content = initial_post_post_data.get('content', initial_post_post.content)
            initial_post_post.save()

        if 'reference_file' in validated_data:
            reference_file_data = validated_data.pop('reference_file')
            reference_file = ReferenceFile.objects.filter(thread=instance)
            for ref in reference_file:
                for ref_data in reference_file_data:
                    ref.title = ref_data.get('title', ref.title)
                    ref.url = ref_data.get('url', ref.url)
                ref.save()

        # if 'discussion_guide' in validated_data:
        #     discussion_guide_data = validated_data.pop('discussion_guide')
        #     discussion_guide = instance.discussion_guide
        #     discussion_guide.deadline = discussion_guide_data.get('deadline', discussion_guide.deadline)
        #     discussion_guide.description = discussion_guide_data.get('description', discussion_guide.description)
        #     discussion_guide.mechanism_expectation = discussion_guide_data.get('mechanism_expectation', discussion_guide.mechanism_expectation)
        #     discussion_guide.save()

        instance.title = validated_data.get('title', instance.title)
        instance.save()

        return instance

class ThreadResponseSerializer(serializers.ModelSerializer): #buat tampilan di week
    initial_post = InitialPostWeekThreadSerializer(read_only=True)
    # discussion_guide = DiscussionGuideWeekThreadSerializer(read_only=True)
    
    class Meta:
        model = Thread
        fields = ('id', 'title', 'deadline', 'description', 'mechanism_expectation', 'summary_content', 'initial_post')

class WeekSerializer(serializers.ModelSerializer):
    threads = ThreadResponseSerializer(read_only=True,many=True)
    class Meta:
        model = Week
        fields = ('id','name','threads')

class DiscussionAnalyticsSerializer(serializers.Serializer):
    replies = serializers.IntegerField()
    participants = serializers.IntegerField()
    non_participants = serializers.IntegerField()
    tags = serializers.DictField()

class BreadcrumbSerializer(serializers.ModelSerializer):
    week_name = serializers.ReadOnlyField()
    class Meta:
        model = Thread
        fields = ('id', 'week_name')
