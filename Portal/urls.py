from Portal.views import get_completions, index
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('tinymce/', include('tinymce.urls')),
    path("register", views.register_request, name="register"),
    path("homepage", views.homepage, name="homepage"),
    path("get_completions/", views.get_completions, name="get_completions")
]
