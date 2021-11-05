from django.db import models
from accounts.models import CITIES, Customer
from django.core.validators import MaxValueValidator, MinValueValidator


TYPE = (('C', 'Car'), ('A', 'Appartments'))


class Tag(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name}_tag'

class Service(models.Model):

    title = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True, choices=TYPE)
    price_ah = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    sh_desc = models.CharField(max_length=30, blank=True, null=True)
    desc = models.TextField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=1, blank=True, null=True, choices=CITIES)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class OrderHistory(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Service, on_delete=models.CASCADE)
    done_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username}__{self.item.title}'


class Feedback(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Service, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        unique_together = ['user', 'item']

    def __str__(self):
        return f'{self.user}_{self.item}_feed'