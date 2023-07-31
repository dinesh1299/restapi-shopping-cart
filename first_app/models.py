from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(null=True,blank=True)        

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, blank=True,null=True,related_name='product')
    name = models.CharField(max_length=100,null=True, blank=True)
    price = models.CharField(max_length=100,null=True, blank=True)
    rating = models.FloatField(default=0)
    total_rating_sum = models.FloatField(default=0)
    num_of_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True,null=True,related_name='order')
    dateOrdered=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

def validate_less_than_or_equal_to_five(value):
    if value > 5:
        raise ValidationError(
            _("Value must be less than or equal to five."),
            code='greater_than_five'
        )

class Ratings(models.Model):
    rating = models.IntegerField(validators=[validate_less_than_or_equal_to_five])
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True,null=True,related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.product.name}_{self.rating}'
    

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True,null=True)
    quantity=models.IntegerField(default=1)
    dateAdded=models.DateTimeField(auto_now_add=True)
        
    # def __str__(self):
    #    return f'{self.product.name}, Order number {self.id}'
 