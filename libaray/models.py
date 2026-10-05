from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    published_data= models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.title
    