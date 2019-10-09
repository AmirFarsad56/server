from django.db import models
from django.conf import settings

class CommonUserModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                               related_name='commonusers', primary_key = True)
    phone_number = models.CharField(max_length = 20, null = True, blank = False ,unique = True)

    def __str__(self):
        return self.user.username
