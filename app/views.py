from urllib.parse import urlparse
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import get_token
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseGone
from django.contrib.auth import authenticate
from .models import Url
from rest_framework.permissions import IsAuthenticated
from django.views.generic import RedirectView
from .serializers import (
    UrlSer,
    UserLoginSer,
    UserRegisterSer,
)
from drf_spectacular.utils import extend_schema


class UserRegisterView(APIView):
    @extend_schema(request=UserRegisterSer, responses={201: dict})
    def post(self, request):
        serializer = UserRegisterSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_token(user)
        return Response({'token': tokens}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    @extend_schema(request=UserLoginSer, responses={200: dict, 400: dict})
    def post(self, request):
        serializer = UserLoginSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_token(user)
            return Response({'token': token})
        return Response({'msg': 'Invalid credentials'}, status=400)


class ShortUrlView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=UrlSer, responses={201: UrlSer})
    def post(self, request):
        serializer = UrlSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.save(user=request.user)
        return Response({
            'original_url': url.original_url,
            'short_url': request.build_absolute_uri(f'/{url.short_url}/'),
        }, status=status.HTTP_201_CREATED)



class ListUrlView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UrlSer(many=True))
    def get(self, request):
        urls = Url.objects.filter(user=request.user).order_by('-created_at')
        serializer = UrlSer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class UrlRedirectView(RedirectView):

    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, short_url=kwargs['short_code'], is_active=True)
        return url.original_url