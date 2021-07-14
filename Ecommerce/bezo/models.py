from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICE = (('andhra pradesh', 'ANDHRA PRADESH'),
                ('arunachal pradesh', 'ARUNACHAL PRADESH'),
                ('assam', 'ASSAM'),
                ('bihar', 'BIHAR'),
                ('chhattisgarh', 'CHHATTISGARH'),
                ('goa', 'GOA'),
                ('gujarat', 'GUJARAT'),
                ('haryana', 'HARYANA'),
                ('himachal pradesh', 'HIMACHAL PRADESH'),
                ('jharkhand', 'JHARKHAND'),
                ('karnataka', 'KARNATAKA'),
                ('kerala', 'KERALA'),
                ('madhya pradesh', 'MADHYA PRADESH'),
                ('maharashtra', 'MAHARASHTRA'),
                ('manipur', 'MANIPUR'),
                ('imphal', 'IMPHAL'),
                ('meghalaya', 'MEGHALAYA'),
                ('mizoram', 'MIZORAM'),
                ('nagaland', 'NAGALAND'),
                ('odisha', 'ODISHA'),
                ('punjab', 'PUNJAB'),
                ('rajasthan', 'RAJASTHAN'),
                ('sikkim', 'SIKKIM'),
                ('tamil nadu', 'TAMIL NADU'),
                ('telangana', 'TELANGANA'),
                ('tripura', 'TRIPURA'),
                ('uttar pradesh', 'UTTAR PRADESH'),
                ('uttarakhand', 'UTTARAKHAND'),
                ('west bengal', 'WEST BENGAL'))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=222)
    city = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=100)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICE = (('TW', 'Top Wear'),
                   ('BW', 'Bottom Wear'),
                   ('LT', 'Loptop'),
                   ('MP', 'Mobile Phone'))


class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=100)
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

STATUS_CHOICES = (('Accepted', 'Accepted'),
                  ('Packed', 'Packed'),
                  ('On The Way', 'On The Way'),
                  ('Delivered', 'Delivered'),
                  ('Cancel', 'Cancel'))

class OrederPlaced(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price