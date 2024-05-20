from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)


class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
