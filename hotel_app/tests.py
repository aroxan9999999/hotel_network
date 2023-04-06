import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from hotel_app.models import Tour, Hotel, Hotel_number
from users.models import Number

User = get_user_model()


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hotel = Hotel.objects.create(name='test hotel', image='../media/Hotel/accommodation_1.png', price=555,
                                         country='Armenia')
        cls.tour = Tour.objects.create(title="Остров бонда", place=200, price=500, hotel=cls.hotel)
        cls.hotel_number = Hotel_number.objects.create(hotel=cls.hotel,
                                                       number_image='../media/Hotel/_number/number_1.jpg', price=500)
        cls.user = User.objects.create(username="Test", email='aroxan.999@mail.ru', password='123', phone='37497713011',
                                       many=0)
        cls.user2 = User.objects.create(username="Test2", email='aroxan.9999@mail.ru', password='123',
                                        phone='37497713012',
                                        many=10000)
        cls.tourist = 2
        cls.nights = 2

    def test__index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test__book_hotel_tour(self):
        response = self.client.post(reverse('index'),
                                    {'country': 'Armenia', 'fly': 'Stepanakert',
                                     'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                     'tourist': self.tourist, 'nights': self.nights, 'tour': self.tour.title,
                                     'username': self.user.username})
        if self.user.many < self.tour.price * self.tourist * self.nights:
            self.assertEqual(response.url, '/payment/')
            self.assertEqual(response.status_code, 302)

    def test__user_2(self):
        response = self.client.post(reverse('index'),
                                    {'country': 'Armenia', 'fly': 'Stepanakert',
                                     'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                     'tourist': self.tourist, 'nights': self.nights, 'tour': self.tour.title,
                                     'username': self.user2.username})
        self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 302)

    def test__number_detail_get(self):
        response = self.client.get(reverse('number_detail', args=(self.hotel_number.pk,)))
        self.assertEqual(response.status_code, 200)

    def test__number_detail_post(self):
        response = self.client.post(reverse('number_detail', args=(self.hotel_number.pk,)),
                                    {'username': self.user2.username})
        self.assertEqual(response.status_code, 302)

    def test_number_detail_content(self):
        response = self.client.get(f'/number/{self.hotel_number.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.hotel.name, response.content.decode())
