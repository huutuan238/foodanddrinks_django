from django.test import TestCase
from django.urls import reverse
from ..models import Order, OrderDetail, User, Product, Category, Customer

DEFAULT_AVATAR = 'media/profile_pics/default.jpg'
DEFAULT_IMAGE = 'media/product_pics/coffe.jpeg'

class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Drinks')
        Product.objects.create(name='milk tea', category_id=1, price=23.00, quantity=10, vote=3.0,
                               description='made in VN')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name = "Drinks")
        number_of_products = 6
        for product_id in range(number_of_products):
          Product.objects.create(
            name=f'product{product_id}',
            category = category,
            description= "test product",
            price= 2.00,
            quantity=10,
            vote= 5.0,
            image= DEFAULT_IMAGE,
          )

    def test_view_url_exits_at_desired_location(self):
      response = self.client.get('/restaurant/')
      self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
      response = self.client.get(reverse('index'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'index.html')

    def test_pagination_is_four(self):
      response = self.client.get(reverse('index'))
      self.assertEqual(response.status_code, 200)
      self.assertTrue(len(response.context['page_obj']) == 4)

    def test_lists_all_products(self):
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['page_obj']) == 2)


class CatagoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_categories = 5

        for category_id in range(number_of_categories):
            Category.objects.create(
              name = f' Tra Sua {category_id}',
            )

        number_of_products = 5
        for product_id in range(number_of_products):
          Product.objects.create(
            name=f'product{product_id}',
            category = Category.objects.get(id =1),
            description= "test product",
            price= 2.00,
            quantity=10,
            vote= 5.0,
            image= DEFAULT_IMAGE,
          )

    def test_view_url_exists_at_desired_location(self):
        category = Category.objects.get(id=1)
        url = reverse('product_by_category', args=[str(category.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        category = Category.objects.get(id=1)
        url = reverse('product_by_category', args=[str(category.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
      category = Category.objects.get(id=1)
      url = reverse('product_by_category', args=[str(category.id)])
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'product_by_category.html')

    def test_pagination_is_three(self):
      category = Category.objects.get(id=1)
      url = reverse('product_by_category', args=[str(category.id)])
      response = self.client.get(url)
      self.assertEqual(response.status_code, 200)
      self.assertTrue(len(response.context['page_obj']) == 3)

    def test_lists_all_catagories(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        category = Category.objects.get(id=1)
