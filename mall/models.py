from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category_level = models.IntegerField()
    parent_level_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='main_category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    price = models.FloatField()
    is_valid = models.BooleanField(default=True)
    creat_time = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'merchandise'
        verbose_name = 'Merchandise'
        verbose_name_plural = 'Merchandises'


class MerchandiseDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    discount = models.FloatField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.merchandise.name

    class Meta:
        db_table = 'merchandise_discount'
        verbose_name = 'MerchandiseDiscount'


class MerchandiseRating(models.Model):
    id = models.AutoField(primary_key=True)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    ratings = models.FloatField()
    no_of_ratings = models.IntegerField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.merchandise.name

    class Meta:
        db_table = 'merchandise_rating'
        verbose_name = 'MerchandiseRating'
