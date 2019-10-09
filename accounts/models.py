from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings

class UserModel(AbstractUser):
    first_name = models.CharField(max_length=216, null = False, blank = False)
    last_name = models.CharField(max_length=216, null = False, blank = False)
    is_sportclub = models.BooleanField('SportClub Status', default = False)
    is_commonuser = models.BooleanField('CommonUser Status', default = False)
    is_masteruser = models.BooleanField('MasterUser Status', default = False)
    email = models.EmailField(unique = True, blank = False)
    slug = models.SlugField(unique = True, null = False, blank = False)
    picture = models.ImageField(upload_to =r'superuser/coverpicture',
                                null = True, blank = True, default = r'superuser/default/Koala.jpg')
    user_logs = models.TextField(default='',null = True)

    def save(self, *args, **kwargs):

        try:
            name = self.picture.name.lower()
            if name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg'):
                pass
            else:
                self.picture = None
        except:
            pass
        super(UserModel, self).save(*args, **kwargs)
