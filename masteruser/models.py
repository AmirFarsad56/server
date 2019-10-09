from django.db import models
from django.conf import settings


class MasterUserModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                               related_name='masterusers', primary_key = True)
    phone_number = models.CharField(max_length = 20, blank = False, null = False, unique = True)
    picture = models.ImageField(default = r'masteruser/default/default_masteruser.jpg',
                                 upload_to=r'masteruser/coverpicture')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.picture.name.endswith('.jpg') or self.picture.name.endswith('.png') or self.picture.name.endswith('.jpeg'):
            pass
        else:
            self.picture = None
        super(MasterUserModel, self).save(*args, **kwargs)    
