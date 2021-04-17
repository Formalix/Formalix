from Portal.views import index
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('tinymce/', include('tinymce.urls')),
    path("register", views.register_request, name="register"),
    path("homepage", views.homepage, name="homepage")
]
