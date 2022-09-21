from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
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


class APITesting(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="kim@salistech.com",
            first_name="kim",
            last_name="kim",
            password="asj4hg@bvg123",
            gender="male",
            phone="09098765434",
        )
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        self.price = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        self.product = Product.objects.create(
            category=self.category,
            price=self.price,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )

    def test_list_products_endpoint(self):
        """Test to list products endpoint."""

        price2 = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        Product.objects.create(
            category=self.category,
            price=price2,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        result = self.client.get("/api/v1/products/")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_categories_endpoint(self):
        """Test to list categories endpoint."""

        Category.objects.create(
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        result = self.client.get("/api/v1/categories/")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 2)

    def test_get_single_product_endpoint(self):
        """Test to get a single product endpoint."""

        result = self.client.get(f"/api/v1/product-detail/{self.product.slug}/")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_list_products_by_category_endpoint(self):
        """Test to list products by category endpoint."""

        price2 = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        Product.objects.create(
            category=self.category,
            price=price2,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        result = self.client.get(f"/api/v1/products/{self.category.slug}/category/")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)

    def test_search_endpoint(self):
        """Test search endpoint."""

        price2 = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        Product.objects.create(
            category=self.category,
            price=price2,
            title="Software",
            description="Software description",
            image=get_test_image_file()
        )
        query = "software"
        result = self.client.get(f"/api/v1/search?query={query}")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_order_endpoint(self):
        """Test to order endpoint."""

        result = self.client.post(f"/api/v1/order/{self.product.slug}/")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_order_history_endpoint(self):
        """Test order history endpoint."""

        price2 = Price.objects.create(
            currency="NGN",
            amount=Decimal("234")
        )
        product2 = Product.objects.create(
            category=self.category,
            price=price2,
            title="sport",
            description="Sport description",
            image=get_test_image_file()
        )
        self.client.post(f"/api/v1/order/{self.product.slug}/")
        self.client.post(f"/api/v1/order/{product2.slug}/")

        result = self.client.get(f"/api/v1/order-history/")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 2)
