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

class NestedReplyPostViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = NestedReplyPost.objects.all()
    serializer_class = NestedReplyPostSerializer

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
        first = False
        if request.user not in initial_post.seen.all():
            initial_post.seen.add(request.user)
            first = True
        seen = []
        for user in initial_post.seen.all():
            custom_user = CustomUser.objects.get(user=user)
            seen.append({
                "user_id": user.id,
                "name":custom_user.name,
                "role": custom_user.role,
                "group": custom_user.group.name if custom_user.group else None,
                "photo_url":custom_user.photo_url
            })
        return Response(InitialPostSeenSerializer({"seen": seen, "first": first}).data)
