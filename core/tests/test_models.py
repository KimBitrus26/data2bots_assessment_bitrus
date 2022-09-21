from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.core.files.temp import NamedTemporaryFile
from django.core import files

from core.models import Price, Product, Order, Category


User = get_user_model()


def get_test_image_file():
    image_temp_file = NamedTemporaryFile(delete=True)
    file_name = 'temp.jpg'
    image_temp_file.flush()
    temp_file = files.File(image_temp_file, name=file_name)
    return temp_file


class ModelBusinessTests(TestCase):

    def test_create_price_model(self):
        """Test create price instance"""

        price = Price.objects.create(
                    currency="NGN",
                    amount=Decimal("234")
                )
        self.assertTrue(isinstance(price, Price))
        self.assertEqual(Price.objects.count(), 1)
        self.assertEqual(str(price), str(price.amount))

    def test_create_category_model(self):
        """Test create category instance"""

        category = Category.objects.create(
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(str(category), f"{category.id} - {category.title}")

    def test_create_product_model(self):
        """Test create product instance"""

        category = Category.objects.create(
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        price = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        product = Product.objects.create(
            category=category,
            price=price,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(str(product), f"{product.id} - {product.title}")

    def test_create_order_model(self):
        """Test create product instance"""

        category = Category.objects.create(
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        price = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        product = Product.objects.create(
            category=category,
            price=price,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        user = User.objects.create_user(
                email="kim@salistech.com",
                first_name="kim",
                last_name="kim",
                password="asj4hg@bvg123",
                gender="male",
                phone="09098765434",
                        )
        order = Order.objects.create(
                                product=product,
                                user=user
        )
        self.assertTrue(isinstance(order, Order))
        self.assertEqual(Order.objects.count(), 1)
