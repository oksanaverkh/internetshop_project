from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField(
        null=True, blank=True, default=None, upload_to='products_images/')

    def __str__(self):
        return f'Product: {self.name}, price: {self.price}, available quantity: {self.quantity}'


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f'Client: {self.name}, email: {self.email}, telephone: {self.telephone}'

    def set_password(self, password):
        self.password = make_password(password)
        self.save(update_fields=['password'])


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart_item_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'CartItem: {self.product}, quantity: {self.quantity}, cart_item_price: {self.cart_item_price}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)

    def add_item(self, product, quantity):
        cart_item_price=product.price*quantity
        if not self.products.filter(product=product).exists():
            cart_item = CartItem.objects.create(
                cart=self, product=product, quantity=quantity, cart_item_price=cart_item_price)
            self.products.add(cart_item)
        else:
            existing_item = self.products.get(product=product)
            existing_item.quantity += quantity
            existing_item.cart_item_price += existing_item.price*quantity
            existing_item.save()

    def remove_item(self, product):
        if self.products.filter(product=product).exists():
            self.products.get(product=product).delete()

    def clear(self):
        self.products.all().delete()

    def get_total_quantity(self):
        return sum([product.quantity for product in self.products.all()])

    def get_total_price(self):
        return sum([product.cart_item_price for product in self.products.all()])
    
    
    def __str__(self):
        return f'Cart: {self.user}, products: {self.products}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=100, default=None)
    payment_option = models.CharField(max_length=50, default=None)
    status = models.CharField(max_length=50, default='не создан')

    def __str__(self):
        return f'Order: customer: {self.user}, total price: {self.total_price}, order date: {self.order_date}, order status: {self.status}\n'
