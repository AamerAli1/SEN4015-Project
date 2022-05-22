from datetime import datetime
from django.db import models
from django.urls import  reverse
from django.contrib.auth.models import AbstractUser

import datetime
import os

# Create your models here.



class CATEGORY_CHOICES(models.Model):
    name= models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


    class Meta:
           verbose_name_plural = 'Categories'

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
        

    def get_absolute_url(self):
        return reverse('product_catalog_app:product_by_category', args=[self.slug])
    def __str__(self):
        return self.name



def filepath(request,filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%W')
    filename = "%s%s" % (timeNow, old_filename)
    return filename





from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField




class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Movie(models.Model):
    title = models.CharField(max_length=100)
    itemNumber = models.CharField(null = True, max_length=100)
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(CATEGORY_CHOICES,on_delete=models.CASCADE,null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=filepath,null=True, blank = True)

    def __str__(self):
        return self.title + " " +  self.itemNumber

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class list(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    added = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null= True)

    def __str__(self):
        return  self.movie.title + " on " + self.date_added.strftime("%y/%m/%d")



class MovieList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    movies = models.ManyToManyField(list)
    start_date = models.DateTimeField(auto_now_add=True)
    date_added = models.DateTimeField()
    added = models.BooleanField(default=False)

   
   
 

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.movies.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
