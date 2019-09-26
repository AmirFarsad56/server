from django.db import models
from django.conf import settings

class CommonUserModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                               related_name='commonusers', primary_key = True)
    phone_number = models.CharField(max_length = 20, null = True, blank = False ,unique = True)
    picture = models.ImageField(default = r'commonuser/default/default_commonuser.jpg',
                                 upload_to=r'commonuser/coverpicture')
    #booked_times = models.ForeignKey()
    #interests

    def __str__(self):
        return self.user.username
