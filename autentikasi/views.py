from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings

from .serializers import *
from .models import CustomUser

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        custom_user = CustomUser.objects.get(user=user)
        return Response(LoginResponseSerializer({
            "token": token.key,
            "user_id": user.id, 
            "role": custom_user.role,
            "group": custom_user.group.id if custom_user.group else None,
            "photo_url": custom_user.photo_url
            }).data)
    
class LogoutView(views.APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ProfileView(views.APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        try:
            custom_user = CustomUser.objects.get(user=request.user)
            if (custom_user.role == 'lecturer'):
                lecturer = Lecturer.objects.get(lecturer=custom_user)
                return Response(ProfileSerializer({
                    "user_id": request.user.id,
                    "name":custom_user.name,
                    "nim":lecturer.nim,
                    "group": None,
                    "photo_url":custom_user.photo_url,
                }).data)
            elif (custom_user.role == 'student'):
                student = Student.objects.get(student=custom_user)
                return Response(ProfileSerializer({
                    "user_id": request.user.id,
                    "name":custom_user.name,
                    "nim":student.npm,
                    "group": custom_user.group.name if custom_user.group else None,
                    "photo_url":custom_user.photo_url,
                }).data)
        except CustomUser.DoesNotExist or Lecturer.DoesNotExist or Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    
        return Response(status=status.HTTP_404_NOT_FOUND) 

    def put(self, request):
        try:
            custom_user = CustomUser.objects.get(user=request.user)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCustomUserPhotoRequestSerializer(custom_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LecturerView(views.APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        lecturers = Lecturer.objects.all()
        return Response(LecturerSerializer(lecturers, many=True).data)
    
class CustomGroupViewSet(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer