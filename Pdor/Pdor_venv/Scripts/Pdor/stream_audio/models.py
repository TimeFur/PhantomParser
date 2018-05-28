# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Stream_DB(models.Model):
    title = models.CharField(max_length = 50)
    url = models.TextField(blank = True)
    photo = models.URLField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
