from Portal.views import get_completions, index, edit, editDetail
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('edit/', views.edit, name = 'edit'),
    path('editDetail/<int:document_id>/', views.editDetail, name = 'editDetail'),
    path('deleteDocument/<int:document_id>/', views.deleteDocument, name = 'editDetail'),
    path('genDoc/', views.genDoc, name="genDoc"),
    path('genTex/', views.genTex, name="genTex"),
    path('tinymce/', include('tinymce.urls')),
    path("register", views.register_request, name="register"),
    path("homepage", views.homepage, name="homepage"),
    path("get_completions/", views.get_completions, name="get_completions")
]
