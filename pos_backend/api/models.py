from django.db import models
from django.contrib.auth.hashers import make_password, check_password as django_check_password


class AuthAdmin(models.Model):
    """
    Separate admin authentication table (auth_admin).
    Created automatically when running: python manage.py createadmin
    """
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)  # Stored as hashed password
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_admin'
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.name} ({self.email})"

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check a raw password against the stored hash."""
        return django_check_password(raw_password, self.password)


class Product(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pos_products'

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    product_name = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pos_inquiries'

    def __str__(self):
        return f"{self.name} - {self.product_name}"
