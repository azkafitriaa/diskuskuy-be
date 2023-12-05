from rest_framework import views
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings

from .serializers import *
from .models import *

class BreadcrumbViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = Thread.objects.all()
    serializer_class = BreadcrumbSerializer

class WeekViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = Week.objects.all()
    serializer_class = WeekSerializer

class ThreadViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = Thread.objects.all()
    serializer_class = ThreadRequestSerializer

class ReferenceFileViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = ReferenceFile.objects.all()
    serializer_class = ReferenceFileRequestSerializer

class DiscussionAnalytics(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, thread_id):
        replies, participants = [], []
        non_participants_count, replies_count, nested_replies_count = 0, 0, 0
        tags = {}

        initial_post = get_object_or_404(InitialPost.objects.all(), thread=thread_id)
        replies = ReplyPost.objects.filter(initial_post=initial_post.id)
        replies_count = ReplyPost.objects.filter(initial_post=initial_post.id).count()
        
        for reply in replies:
            reply_post = reply.post
            reply_post_creator = reply_post.creator

            if reply_post_creator not in participants:
                participants.append(reply_post_creator)

            reply_post_tags = reply_post.tag.lower().split(',')
            for reply_post_tag in reply_post_tags:
                if reply_post_tag not in tags.keys():
                    tags[reply_post_tag] = 1
                else:
                    tags[reply_post_tag] += 1

            nested_replies_count += NestedReplyPost.objects.filter(reply_post=reply.id).count()
            nested_replies = NestedReplyPost.objects.filter(reply_post=reply.id)

            for nested_reply in nested_replies:
                nested_reply_post = nested_reply.post
                nested_reply_post_creator = nested_reply_post.creator

                if nested_reply_post_creator not in participants:
                    participants.append(nested_reply_post_creator)

                nested_reply_post_tags = nested_reply_post.tag.lower().split(',')
                for nested_reply_post_tag in nested_reply_post_tags:
                    if nested_reply_post_tag not in tags.keys():
                        tags[nested_reply_post_tag] = 1
                    else:
                        tags[nested_reply_post_tag] += 1

        non_participants_count = len(CustomUser.objects.all()) - len(participants)

        return Response(DiscussionAnalyticsSerializer({
            "replies": replies_count + nested_replies_count, 
            "participants": len(participants), 
            "non_participants": non_participants_count,
            "tags": tags
            }).data)
    
class ThreadThisMonthView(views.APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        now = datetime.now()
        threads = Thread.objects.filter(deadline__month=now.month)
        print(threads)
        return Response(ThreadResponseSerializer(threads, many=True).data)
    
class ThreadTodayView(views.APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        now = datetime.now()
        threads = Thread.objects.filter(deadline__day=now.day)
        return Response(ThreadResponseSerializer(threads, many=True).data)
    