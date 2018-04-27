from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    bdate = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=200, db_index=True)
    phoneNumber = models.IntegerField(default=1234567890)
    address = models.CharField(max_length=250,default=None)
    city = models.CharField(max_length=250,default=None)
    country = models.CharField(max_length=250, default=None)
    zipcode = models.IntegerField(default=12345)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
