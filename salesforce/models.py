from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)#cascade mtlb jb user delete hua to cust b del ho jaey ga
    name = models.CharField(max_length=22)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default="download.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return str(self.name)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#
#     if created:
#         Customer.objects.create(user=instance)
#         print("profile created")
#
# #post_save.connect(create_profile, sender=User)
#
# @receiver(post_save, sender=User)
# def update_profile(sender, instance, created, **kwargs ):
#
#     if created== False:
#         instance.customer.save()
#         print("profile updated")


#post_save.connect(update_profile, sender=User)


class Tags(models.Model):
    name = models.CharField(max_length=22)


    def __str__(self):
       return self.name


class Product(models.Model):
    Category = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )
    name = models.CharField(max_length=22)
    price = models.FloatField()
    category = models.CharField(max_length=20, choices=Category)
    description = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
       return self.name



class Order(models.Model):
    Status = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer , null=True, on_delete=models.SET_NULL)#mtlb jb parent customer delete ho to child save e rhy
    product = models.ForeignKey(Product , null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status)
    note = models.CharField(max_length=20, null=True)


    def __str__(self):
       return self.product.name