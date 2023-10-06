from django.shortcuts import render, redirect
import requests
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.conf import settings
from django.contrib.auth.models import User
from .serializers import UserSerializer
# UserProfileSerializer, SecureUserSerializer
# from .models import UserProfile

import random
import string
import re

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    # user_profile = UserProfile.objects.get(user=user)
    # user_profile_serializer = UserProfileSerializer(user_profile)
    user_serializer = UserSerializer(user)
    res = Response(user_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token), samesite='None', secure=True)
    res.set_cookie('access_token', value=str(token.access_token), samesite='None', secure=True)
    return res

# def generate_random_string(length=8):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     random_string = ''.join(random.choice(characters) for _ in range(length))
#     return random_string

# def check_valid_username(username):
#     validator = UnicodeUsernameValidator()
#     try:
#         validator(username)
#         return True
#     except:
#         return False
    
# def remove_special_characters(input_string):
#     # 정규표현식으로 특수문자를 찾아서 제거
#     return re.sub(r'[^\w]', '', input_string)

# Create your views here.   
class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
   
        return set_token_on_response_cookie(user)

    
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username = request.data['username'],
                password = request.data['password']
            )
        except:
            return Response({"detail": "사용자 이름 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh']
        try:
            RefreshToken(refresh_token).verify()
        except:
            return Response({"detail" : "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        new_access_token = str(RefreshToken(refresh_token).access_token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', value=str(new_access_token))
        return response
    
class UserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if request.data['email'] != user.email:
            return Response({"detail": "email should not be changed."}, status=status.HTTP_400_BAD_REQUEST)
        if request.data['username'] != user.username:
            return Response({"detail": "username should not be changed."}, status=status.HTTP_400_BAD_REQUEST)
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"detail": "user data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        # userprofile = user.userprofile
        if request.data['password'] == user.password:
            return Response({"detail": "password match."}, status=status.HTTP_200_OK)
        # else:
        #     if userprofile.socials_id != "a":
        #         return Response({"detail": "socials login user is not allowed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        #     return Response({"detail": "password doesn't match."}, status=status.HTTP_400_BAD_REQUEST)


