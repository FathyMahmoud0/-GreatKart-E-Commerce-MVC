from django.db import models
from category.models import Category
# Create your models here.
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=300,unique=True)
    slug = models.SlugField(max_length=300,unique=True)
    discription = models.TextField(max_length=600,blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=3)
    image = models.ImageField(upload_to='photos/products',default='default.jpg')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modifaied_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('product_detail' , args = [self.category.slug  , self.slug])
    
varition_category_choices = {
    'color' : 'color',
    'size' : 'size',
}   
    
class Varition(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    varition_category = models.CharField(max_length=60 , choices=varition_category_choices)
    varition_value = models.CharField(max_length=30)
    data_created = models.DateTimeField(auto_now_add=True)
    