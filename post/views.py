from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class InitialPostViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = InitialPost.objects.all()
    serializer_class = InitialPostSerializer

class ReplyPostViewSet(viewsets.ModelViewSet):    
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = ReplyPost.objects.all()
    serializer_class = ReplyPostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        initial_post = get_object_or_404(InitialPost.objects.all(), pk=data['initial_post'])
        post_data = data['post']
        creator = get_object_or_404(User.objects.all(), pk=post_data['creator'])
        post = Post(
            tag=post_data['tag'],
            content=post_data['content'],
            creator=creator,
        )
        post.save()
        reply_post = ReplyPost(
            post=post,
            initial_post=initial_post
        )
        reply_post.save()
        thread = get_object_or_404(Thread.objects.all(), initial_post=data['initial_post'])
        if request.user not in thread.user_done.all():
            thread.user_done.add(request.user)
        return Response(status=200)

class NestedReplyPostViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = NestedReplyPost.objects.all()
    serializer_class = NestedReplyPostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        reply_post = get_object_or_404(ReplyPost.objects.all(), pk=data['reply_post'])
        post_data = data['post']
        creator = get_object_or_404(User.objects.all(), pk=post_data['creator'])
        post = Post(
            tag=post_data['tag'],
            content=post_data['content'],
            creator=creator,
        )
        post.save()
        nested_reply_post = NestedReplyPost(
            post=post,
            reply_post=reply_post
        )
        nested_reply_post.save()
        initial_post = get_object_or_404(InitialPost.objects.all(), pk=reply_post.initial_post.id)
        thread = get_object_or_404(Thread.objects.all(), initial_post=initial_post)
        if request.user not in thread.user_done.all():
            thread.user_done.add(request.user)
        return Response(status=200)

class PostLikeViewSet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            if request.user not in post.likes.all():
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostClapViewSet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            if request.user not in post.claps.all():
                post.claps.add(request.user)
            else:
                post.claps.remove(request.user)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostLoveViewSet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            if request.user not in post.loves.all():
                post.loves.add(request.user)
            else:
                post.loves.remove(request.user)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InitialPostSeenViewSet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, pk, format=None):
        try:
            initial_post = InitialPost.objects.get(pk=pk)
        except InitialPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # first = False
        if request.user not in initial_post.seen.all():
            initial_post.seen.add(request.user)
            # first = True
        return Response(CustomUserSerializer(initial_post.seen_user_info, many=True).data)
        # seen = []
        # for user in initial_post.seen.all():
        #     custom_user = CustomUser.objects.get(user=user)
        #     seen.append({
        #         "user_id": user.id,
        #         "name":custom_user.name,
        #         "role": custom_user.role,
        #         "group": custom_user.group.name if custom_user.group else None,
        #         "photo_url":custom_user.photo_url
        #     })
        # return Response(InitialPostSeenSerializer({"seen": seen, "first": first}).data)
