from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from hotel_app.models import Hotel, Hotel_number


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=255)
    many = models.BigIntegerField(default=0, blank=True, null=True)
    billet = models.OneToOneField("Billet", on_delete=models.SET_NULL, blank=True, null=True)
    number = models.OneToOneField("Number", on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.billet is None:
            self.billet = Billet.objects.create(price=0)
        if self.number is None:
            self.number = Number.objects.create(price=0)
        super().save(*args, **kwargs)

    def get_many(self):
        return '{0:,}'.format(self.many).replace(',', ' ')


class Billet(models.Model):
    active = models.BooleanField(default=False)
    price = models.IntegerField()
    buy_time = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True)
    billet_time_start = models.DateField(blank=True, null=True)
    billet_time_end = models.DateField(blank=True, null=True)
    numbers_person = models.IntegerField(default=0)

    def __str__(self):
        if self.hotel:
            return self.hotel.name
        return str(self.pk)


class Number(models.Model):
    active = models.BooleanField(default=False)
    price = models.IntegerField()
    buy_time = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        if self.hotel:
            return self.hotel.name
        return str(self.pk)
