from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=150)
    hotel_number = models.ManyToManyField('Hotel_number', related_name='get_hotel_number', blank=True)
    rating = models.SmallIntegerField(default=0)
    image = models.ImageField(upload_to='Hotel')
    price = models.BigIntegerField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)

    def get_format_price(self):
        return '{0:,}'.format(self.price).replace(',', ' ')

    def get_rating(self):
        return ((range(self.rating)), (range(5 - self.rating)))

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = "Hotels"


class Hotel_number(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='get_hotel_object')
    number_image = models.ImageField(upload_to='Hotel/_number')
    price = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    bronny = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.hotel.name

    def get_format_price(self):
        return '{0:,}'.format(self.price).replace(',', ' ')

    class Meta:
        verbose_name = 'номера_отелей'
        verbose_name_plural = 'номера_отелей'


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='Hotel/_service')
    service_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='get_service_to_hotel')

    def __str__(self):
        return self.service_hotel.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = "Услуги"


class Tour(models.Model):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    place = models.IntegerField()
    price = models.BigIntegerField()
    description = models.TextField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='get_tour_object')

    def __str__(self):
        return self.hotel.name

    class Meta:
        verbose_name = 'Tour'
        verbose_name_plural = "Tours"

    def get_format_price(self):
        return '{0:,}'.format(self.price).replace(',', ' ')
