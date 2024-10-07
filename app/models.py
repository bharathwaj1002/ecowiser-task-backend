from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    logo = models.ImageField(upload_to ='brands/', default='')
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Link brand to user


    def __str__(self):
        return self.name
    
class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    picture1 = models.ImageField(upload_to ='products/', default='')
    picture2 = models.ImageField(upload_to ='products/', default='')
    picture3 = models.ImageField(upload_to ='products/', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)   
    
    stock = models.IntegerField()
    def __str__(self):
        return self.name

class Specification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)  # e.g. "Color", "Material"
    value = models.CharField(max_length=200)  # e.g. "Red", "Cotton"

    def __str__(self):
        return f'{self.key}: {self.value}'