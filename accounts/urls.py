from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/register",views.UserRegisterView.as_view(), name = "register_user"),
    path("api/login",views.UserLoginView.as_view(), name = "login_user"),
    path("api/profile",views.ProfileView.as_view(), name = "profile"),
]