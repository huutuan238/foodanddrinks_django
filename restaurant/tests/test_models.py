from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Order, OrderDetail, User, Product, Category, Customer, Comment, Review


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin1 = User.objects.create(is_superuser=1, username="admin1", first_name="hoang", last_name="thanh",
                                    email="admin1@admin1.com", is_staff=1, is_active=1)
        Order.objects.create(total_price=100, status="p", admin_id=admin1.id, customer_id=1,
                             code="2020_9_14_xx")

    def test_checkTotalPrice(self):
        print("Checking total_price field of Order.")
        test_order = Order.objects.get(id=1)
        max_digits = test_order._meta.get_field('total_price').max_digits
        self.assertEquals(max_digits, 6)


class OrderDetailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin2 = User.objects.create(is_superuser=1, username="admin2", first_name="hoang", last_name="thanh",
                                     email="admin2@admin2.com", is_staff=1, is_active=1)
        Order.objects.create(total_price=100, status="p", admin_id=admin2.id, customer_id=1,
                             code="2020_9_14_xx")
        Category.objects.create(name='Drinks')
        Product.objects.create(name='milk tea', category_id=1, price=23.00, quantity=10, vote=3.0,
                               description='made in VN')
        OrderDetail.objects.create(price=10, amount=10, order_id=1, product_id=1)

    def test_checkPrice(self):
        print("Checking price field of OrderDetail.")
        test_orderdetail = OrderDetail.objects.get(id=1)
        max_digits = test_orderdetail._meta.get_field('price').max_digits
        print(max_digits)
        self.assertEquals(max_digits, 4)

class ProductModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    category = Category.objects.create(name = "Drinks")
    Product.objects.create(name="product1", category = category, description= "test product", price= 2, quantity=10, vote= 4)

  def test_name_label(self):
    product = Product.objects.get(id=1)
    field_label = product._meta.get_field('name').verbose_name
    self.assertEquals(field_label, 'name')

  def test_name_max_length(self):
    product = Product.objects.get(id=1)
    max_length=product._meta.get_field('name').max_length
    self.assertEquals(max_length,200)

  def test_object_name_is_name(self):
    product = Product.objects.get(id=1)
    expected_object_name = f'{product.name}'
    self.assertEquals(expected_object_name, str(product))

  def test_get_absolute_url(self):
    product = Product.objects.get(id=1)
    self.assertEquals(product.get_absolute_url(), '/restaurant/product/1')

  def test_price_max_digits(self):
    product = Product.objects.get(id=1)
    max_digits=product._meta.get_field('price').max_digits
    self.assertEquals(max_digits,4)

  def test_price_decimal_places(self):
    product = Product.objects.get(id=1)
    decimal_places=product._meta.get_field('price').decimal_places
    self.assertEquals(decimal_places,2)

  def test_vote_value(self):
    product = Product.objects.get(id=1)
    if float(product.vote)>5:
      raise ValidationError(_('Product rating beyond 5'))
    elif int(product.vote<0):
      raise ValidationError(_('Product rating under 0'))


class CustomerModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username = 'Test', password ='123123@q')
    Customer.objects.create(user = user)

  def test_object_name_is_user_name(self):
    customer = Customer.objects.get(id=1)
    expected_object_name = f'{customer.user.username}'
    self.assertEquals(expected_object_name, str(customer))

class CategoryModelsTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    """Set up non-modified objects used by all test methods."""
    Category.objects.create(name = 'Drinks')

  def test_name_label(self):
    category = Category.objects.get(id = 1)
    field_label =Category._meta.get_field('name').verbose_name
    self.assertEquals(field_label,'name')

  def test_name_max_length(self):
    category = Category.objects.get(id = 1)
    max_length = category._meta.get_field('name').max_length
    self.assertEquals(max_length,200)

class ReviewModelsTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username = 'khach', password ='huutuan0404', is_superuser = 0)
    customer = Customer.objects.create(user = user)
    category = Category.objects.create(name = 'Drinks')
    product = Product.objects.create(name = 'tra sua', category = category, price = 23.00, quantity = 10, vote = 3.0, description = 'nuoc duoc san xuat o vn')
    Review.objects.create(user = customer, product = product,vote = 3, content = 'Nuoc nay rat ngon va bo duong')

  def test_content_label(self):
    review = Review.objects.get(id = 1)
    field_label =review._meta.get_field('content').verbose_name
    self.assertEquals(field_label,'content')

  def test_content_max_length(self):
    review = Review.objects.get(id = 1)
    max_length = review._meta.get_field('content').max_length
    self.assertEquals(max_length,1000)

  def test_vote_value(self):
    review = Review.objects.get(id = 1)
    if int(review.vote) > 5:
        raise ValidationError(_('Review rating beyond 5'))
    elif int(review.vote) <0:
        raise ValidationError(_('Review rating under 0'))

class CommentModelsTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = User.objects.create(username = 'khach', password ='huutuan0404')
    customer = Customer.objects.create(user = user)
    category = Category.objects.create(name = 'Drinks')
    product = Product.objects.create(name = 'tra sua', category = category, price = 23.00, quantity = 10, vote = 3.0, description = 'nuoc duoc san xuat o vn')
    review = Review.objects.create(user = customer, product = product,vote = 3, content = 'Nuoc nay rat ngon va bo duong')
    Comment.objects.create(user = customer, review = review, content = 'cam on ban da ung ho' )

  def test_content_label(self):
    comment = Comment.objects.get(id = 1)
    field_label =comment._meta.get_field('content').verbose_name
    self.assertEquals(field_label,'content')

  def test_content_max_length(self):
    comment = Comment.objects.get(id = 1)
    max_length = comment._meta.get_field('content').max_length

