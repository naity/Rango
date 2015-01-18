from django.test import TestCase

# Create your tests here.
from rango.models import Category
from django.core.urlresolvers import reverse

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        # Every Category should have non-negative reviews
        cat = Category(name="test", views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        # Every Category should have a slug name, which is with dashes and in lowercase
        cat = Category(name="Basic COMPUTER science")
        cat.save()
        self.assertEqual(cat.slug, "basic-computer-science")

from rango.models import Category

def add_category(name, views, likes):
    cat = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return cat

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        # A message should appear if there are no categories in the database
        response = self.client.get(reverse("rango:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context["categories"], [])

    def test_index_view_with_categories(self):
        # Display categories if there are categories in the database
        cat1 = add_category("test1", 1, 1)
        cat2 = add_category("test2", 2, 2)
        cat3 = add_category("test3", 3, 3)
        cat4 = add_category("test4", 4, 4)

        response = self.client.get(reverse("rango:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertContains(response, "test2")
        self.assertContains(response, "test3")
        self.assertContains(response, "test4")
        self.assertQuerysetEqual(response.context["categories"], ["<Category: test4>", "<Category: test3>", 
            "<Category: test2>","<Category: test1>"])