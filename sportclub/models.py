from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as Gmodel


class SportClubModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                                primary_key = True, related_name = 'sportclubs')
    region = models.CharField(max_length = 264, null = False, blank = False)
    phone_number = models.CharField(max_length = 20, blank = True, unique = True)
    serial_number = models.IntegerField(null = False, unique = True)
    company_phone_number = models.CharField(max_length = 20, blank = False)
    sportclub_name = models.CharField(max_length = 264, null = False, blank = False)
    address = models.TextField(blank = False)
    location = Gmodel.PointField(srid = 4326 ,null = True ,blank = True)
    info = models.TextField(blank = True, null= True)
    picture = models.ImageField(default = r'sportclub/default/coverpicture.png',
                                 upload_to=r'sportclub/coverpicture')
    terms_and_conditions = models.TextField(blank = True, null = True)
    bankaccount_ownername = models.CharField(max_length = 300, null = True, blank = True)
    bankaccount_accountnumber = models.CharField(max_length = 30, null = True, blank = True)
    bankaccount_cardnumber = models.CharField(max_length = 30, null = True, blank = True)
    #later these fields can change to iinteger field if need to
    bankaccount_bankname = models.CharField(max_length = 100, null = True, blank = True)
    #this should be a dropdown menu

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):

        try:
            name = self.picture.name.lower()
            if name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg'):
                pass
            else:
                self.picture = None
        except:
            pass
        super(SportClubModel, self).save(*args, **kwargs)
