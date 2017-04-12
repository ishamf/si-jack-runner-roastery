from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.BigIntegerField()

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.ForeignKey('store.Profile')

    items = models.ManyToManyField(CartItem, blank=True)

    def total_price(self):
        return sum(i.total_price() for i in self.items.all())


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    current_cart = models.ForeignKey(Cart, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Purchase(models.Model):
    cart = models.ForeignKey(Cart)
    buyer = models.ForeignKey(Profile)

    resolved = models.BooleanField()

    created_date = models.DateTimeField(auto_now_add=True)

    full_name = models.CharField(max_length=100)
    address = models.TextField()
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    cc = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)
    cc_expiration_date = models.CharField(max_length=100)

    def last_4_cc(self):
        return self.cc[-4:]
