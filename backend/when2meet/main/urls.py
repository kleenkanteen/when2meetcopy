from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', views.UserView.as_view(), name="users"),
    path('events/', views.EventView.as_view(), name="events"),
    path('single/', views.FirstEventView.as_view(), name="single"),
    path('available/', views.AvailableView.as_view(), name="available"),
    path('attendees/', views.AvailableView.as_view(), name="attendees"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 
 
#urlpatterns = format_suffix_patterns(urlpatterns)