from django.db import models

from account.models import User


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
    image = models.ImageField(upload_to="images/", null=True, blank=True , default="images/blank.png")


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
    color = models.ManyToManyField(Color, related_name="product" , blank=True , null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Information(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.CASCADE , related_name="informations")
    text = models.TextField()

    def __str__(self):
        return self.text[:40]



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:40]


class ProductLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)  # True for like, False for dislike
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.fullname} - {self.product.title}"

    class Meta:
        ordering = ['-created']


