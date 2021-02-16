"""My tests."""
from django.test import TestCase, Client
from django import test
from .models import Alias


obj_alias = "test-object"
obj_target = "test-slug-023xf"
new_obj_alias = "test-object1"
test_on_date = "2025-02-15 12:00:05.000000+00:00"


class URLTests(test.TestCase):
    """Applications test."""

    def test_homepage(self):
        """Checking if home page returns response status 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """Creating and checking an object."""
        c = Client()
        response = c.get(f'/create/{obj_alias}/{obj_target}')
        alias_obj = Alias.objects.filter(alias=obj_alias)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(alias_obj.exists())

    def test_create_1(self):
        """Creating and checking an object when the same object exists."""
        self.test_create()
        c = Client()
        response = c.get(f'/create/{obj_alias}/{obj_target}')
        test_content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_content.decode("utf-8") == 'date of new alias overlapping with existing')

    def test_get(self):
        """Checking objects target by now."""
        self.test_create()
        c = Client()
        response = c.get(f'/get/{obj_alias}')
        test_content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_content.decode("utf-8") == 'test-slug-023xf')

    def test_get_on_date(self):
        """Checking objects target by current time."""
        self.test_create()
        c = Client()
        response = c.get(f'/get_on_date/{obj_alias}/{test_on_date}')
        test_content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_content.decode("utf-8") == 'test-slug-023xf')

    def test_alias(self):
        """Checking objects alias by period."""
        self.test_create()
        obj = Alias.objects.get(alias=obj_alias)
        from_datetime = obj.start
        to_datetime = obj.end
        c = Client()
        response = c.get(f'/aliases/{obj_target}/{from_datetime}/{to_datetime}')
        test_content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_content.decode("utf-8") == 'test-object')

    def test_replace(self):
        """Checking replace an existing alias with a new one at a specific time point."""
        self.test_create()
        obj = Alias.objects.get(alias=obj_alias)
        obj_start = obj.start
        c = Client()
        response = c.get(f'/replace/{obj_alias}/{obj_start}/{new_obj_alias}')
        test_content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_content.decode("utf-8") == 'alias created')
