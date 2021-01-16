from django.db import models
from django.contrib.auth.models import User


class UserUrlMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=1024, blank=False)
    is_active = models.BooleanField(default=False)

class DataStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(UserUrlMap, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    header_data = models.TextField(default = "{}")
    form_data = models.TextField(default = "{}")
    is_deleted = models.BooleanField(default=False)

