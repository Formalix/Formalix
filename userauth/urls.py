from Portal.views import get_completions, index
from django.urls import path, include
from . import views
urlpatterns = [
    path('login', views.login_user, name = 'login'),
    path('register', views.register_user, name='register'),
    path("logout", views.logout_user, name="logout"),
]
