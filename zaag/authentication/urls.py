from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication import views

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="user_re"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
]
