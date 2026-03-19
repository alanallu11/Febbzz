from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class Register(models.Model):            
    username=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(12)

class Ladies(models.Model):
    name=models.CharField(max_length=150)
    price=models.IntegerField()
    description=models.CharField(max_length=300)
    image=models.ImageField(upload_to='womenadd/')

    class Meta:
        verbose_name='Ladies'
        verbose_name_plural="Ladies"

class Kids(models.Model):
    kidsname=models.CharField(max_length=100)
    kidsprice=models.IntegerField()
    kidsdescription=models.CharField(max_length=150)
    kidsimage=models.ImageField(upload_to='kidsadd/')

    class Meta:
        verbose_name='Kids'
        verbose_name_plural="Kids"

class Cart(models.Model):
    user = models.CharField(max_length=100)
    ladies_product = models.ForeignKey(Ladies, null=True, blank=True, on_delete=models.CASCADE)
    kids_product = models.ForeignKey(Kids, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ladies_product = models.ForeignKey(Ladies, on_delete=models.CASCADE, null=True, blank=True)
    kids_product = models.ForeignKey(Kids, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist"