from django.db import models

class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title



class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True , null=True , related_name="subs")
    title = models.CharField(max_length=100)
    slug = models.SlugField()


    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ManyToManyField(Category , blank=True , null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    size = models.ManyToManyField(Size , blank=True , null=True ,related_name="product")
    color = models.ManyToManyField(Color, related_name="product")

    def __str__(self):
        return self.title


class Information(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE , related_name="informations")
    text = models.TextField()

    def __str__(self):
        return self.text[:40]

















