from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField
from django.conf import settings

class Document(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    title = CharField(max_length=255)
    reference = TextField(null=True, blank=True)
