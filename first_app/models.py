from django.db import models


class Ad(models.Model):
    username = models.CharField(max_length=15,default='')
    owner_location = models.CharField(max_length=30,default='')
    owner_img = models.ImageField(upload_to="images", default='')
    contact = models.CharField(max_length=11,default='')
    map = models.CharField(max_length=5000,default='')
    category = models.CharField(max_length=50,default='')
    price = models.CharField(max_length=10,default='')
    no_of_room = models.IntegerField(default=0)
    pub_date = models.CharField(max_length=30,default='')
    image1 = models.ImageField(upload_to="images", default='')
    image2 = models.ImageField(upload_to="images", default='')
    image3 = models.ImageField(upload_to="images", default='')
    image4 = models.ImageField(upload_to="images", default='')
    def __str__(self):
            return self.username