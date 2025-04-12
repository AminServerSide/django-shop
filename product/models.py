from django.db import models


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title




class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    size = models.ManyToManyField(Size , blank=True , null=True ,related_name="product")
    color = models.ManyToManyField(Color, related_name="product")

    def __str__(self):
        return self.title