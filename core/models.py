from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from django.conf import settings

from .validators import validate_file

User = settings.AUTH_USER_MODEL


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Price(models.Model):
    """Model to represent Category."""

    NAIRA = "NGN"
    DOLLAR = "USD"
    CURRENCY_CHOICES = (
        (NAIRA, "NGN"),
        (DOLLAR, "USD")
            )
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = int(self.amount * 100)  # save price amount in kobo or cent value
        super().save(*args, **kwargs)


class Category(TimeStampMixin):
    """Model to represent Category."""

    slug = models.SlugField(editable=False)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="assessment/category/images/", validators=[validate_file])

    class Meta(TimeStampMixin.Meta):
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Product(TimeStampMixin):
    """Model to represent Products."""

    slug = models.SlugField(editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="assessment/product/images/", validators=[validate_file])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    price = models.OneToOneField(Price, on_delete=models.CASCADE, related_name="services")

    class Meta(TimeStampMixin.Meta):
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.id} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Order(TimeStampMixin):
    """Model to represent Orders."""

    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    reference = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")

    class Meta(TimeStampMixin.Meta):
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.id} - {self.reference}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify('asmt-{}'.format(str(uuid4()).split('-')[4]))
            self.reference = 'asmt-{}'.format(str(uuid4())[:8])
        super().save(*args, **kwargs)
