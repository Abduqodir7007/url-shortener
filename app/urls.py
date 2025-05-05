from django.urls import path 
from .views import (
    UserLoginView,
    UserRegisterView,
    ShortUrlView,
    UrlRedirectView,
    ListUrlView,
)



urlpatterns = [
    path('register/',UserRegisterView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('shorten/',ShortUrlView.as_view()),
    path('urls/',ListUrlView.as_view()),
    path('<str:short_code>/', UrlRedirectView.as_view()),
    
]   
