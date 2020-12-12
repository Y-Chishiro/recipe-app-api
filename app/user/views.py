# from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # スーパークラスのCreateAPIViewに必要な作業が全て入っているため、
    # ここではシリアライザークラスを指定するだけで良い！！！
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer

    # ブラウザブルAPIにする。POST Methodなので。
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
