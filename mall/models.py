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


class MerchandiseDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    merchandise = models.CharField(max_length=50)
    discount = models.FloatField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'merchandise_discount'
        verbose_name = 'MerchandiseDiscount'


class MerchandiseRating(models.Model):
    id = models.AutoField(primary_key=True)
    merchandise = models.CharField(max_length=50)
    ratings = models.FloatField()
    no_of_ratings = models.IntegerField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'merchandise_rating'
        verbose_name = 'MerchandiseRating'


class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=500, null=True)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='main_category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    price = models.FloatField()
    discount_id = models.ForeignKey(MerchandiseDiscount, on_delete=models.CASCADE, null=True, related_name='discount_id')
    ratings_id = models.ForeignKey(MerchandiseRating, on_delete=models.CASCADE, null=True, related_name='ratings_id')
    is_valid = models.BooleanField(default=True)
    creat_time = models.DateTimeField(default=timezone.now)
    creat_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creat_user', default=1)
    last_update_time = models.DateTimeField(default=timezone.now)
    last_update_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_update_user', default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'merchandise'
        verbose_name = 'Merchandise'
        verbose_name_plural = 'Merchandises'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_time = models.DateTimeField(auto_now_add=True)
