from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}_profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()
