from django.db import models


class Phones(models.Model):
    shop = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    name_lower = models.CharField(max_length=255)
    current_price = models.IntegerField()
    before_discount = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['shop', 'name']
