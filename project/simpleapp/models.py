from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache

class News(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    price = models.FloatField(validators=[MinValueValidator(0.0, 'Price should be >= 0.0')])
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0')])
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='News',
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
