from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create(username="Test", email='aroxan.999@mail.ru', password='123', phone='37497713011',
                                       many=0)

    def test__user_params_default(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.many, 0)
        self.assertEqual(self.user.billet.active, False)
        self.assertEqual(self.user.number.active, False)
        self.assertEqual(self.user.number.price, 0)
        self.assertEqual(self.user.billet.active, False)
