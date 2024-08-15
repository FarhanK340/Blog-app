import os
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.deconstruct import deconstructible

import datetime

# Create your models here.
@deconstructible
class UploadToPath(object):
    def __init__(self, path):
        self.sub_path = path
        
    
    def __call__(self, instance, filename):
        return os.path.join(self.sub_path, filename)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to=UploadToPath('blog/images/'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    

  