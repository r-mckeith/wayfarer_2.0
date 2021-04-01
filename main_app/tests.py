from django.test import TestCase
from .models import City


class PostTestCase(TestCase):
    def testPost(self):
        city = City(name="Chicago", photo_url="http://img.png", slug="Chicago")
        self.assertEqual(city.name, "Chicago")
        self.assertEqual(city.photo_url, "http://img.png")
        self.assertEqual(city.slug, "Chicago")
