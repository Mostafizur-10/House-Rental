from django.db import models
from django.utils import timezone

class Ad(models.Model):
    house_id = models.CharField(max_length=35,default='')
    username = models.CharField(max_length=15,default='') 
    category = models.CharField(max_length=50,default='')
    price = models.CharField(max_length=10,default='')
    no_of_room = models.IntegerField(default=0)
    pub_date = models.CharField(max_length=30,default='')
    datetime = models.DateTimeField(default=timezone.now)
    postal_code = models.IntegerField(default=0)
    description = models.CharField(max_length=20000,default='')
    division = models.CharField(max_length=20,default='')
    district = models.CharField(max_length=20,default='')
    thana = models.CharField(max_length=20,default='')
    union = models.CharField(max_length=20,default='')
    image1 = models.ImageField(upload_to="images", default='')
    image2 = models.ImageField(upload_to="images", default='')
    image3 = models.ImageField(upload_to="images", default='')
    image4 = models.ImageField(upload_to="images", default='')
    value = models.CharField(max_length=10,default='avail')

    def __str__(self):
        return self.house_id

    
class Profile(models.Model):
    username = models.CharField(max_length=15,default='',null=True)
    fname = models.CharField(max_length=20,default='not entered',null=True)
    lname = models.CharField(max_length=20,default='not entered',null=True)
    address = models.CharField(max_length=20,default='not entered',null=True)
    email = models.CharField(max_length=40,default='not entered',null=True)
    phone = models.BigIntegerField(default='',null=True)
    gender = models.CharField(max_length=10,default='',null=True)
    owner_image = models.ImageField(upload_to="images", default='not entered',null=True)

    def __str__(self):
        return self.username