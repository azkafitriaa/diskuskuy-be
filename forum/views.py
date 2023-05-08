from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *

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

class SummaryViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

class DiscussionGuideViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = DiscussionGuide.objects.all()
    serializer_class = DiscussionGuideRequestSerializer

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

@api_view(['GET'])
def discussion_guide_get_by_thread_id(request, thread_id):
    try:
        discussion_guide = get_object_or_404(DiscussionGuide.objects.all(), thread=thread_id)
    except DiscussionGuide.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(DiscussionGuideRequestSerializer(discussion_guide).data)
    return Response(DiscussionGuideRequestSerializer(discussion_guide).errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def discussion_guide_update_state(request, pk):
    try:
        discussion_guide = DiscussionGuide.objects.get(pk=pk)
    except DiscussionGuide.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = DiscussionGuideStateSerializer(discussion_guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ForumOnboardingView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        thread_id = request.GET.get('threadId')
        state = request.GET.get('state')
        if (thread_id and state):
            forum_onboarding = ForumOnboarding.objects.filter(user=request.user, thread=thread_id, state=state)
            if (len(forum_onboarding) > 0):
                return Response(ForumOnboardingSerializer({
                    "show_onboarding": False 
                    }).data)
            else:
                thread = get_object_or_404(Thread.objects.all(), pk=thread_id)
                new_forum_onboarding = ForumOnboarding(
                    user=request.user,
                    thread=thread,
                    state=state
                )
                new_forum_onboarding.save()
                return Response(ForumOnboardingSerializer({
                    "show_onboarding": True 
                    }).data)
        return Response({"threadId and state cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
