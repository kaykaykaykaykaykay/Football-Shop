import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('boots', 'Boots'),
        ('ball', 'Ball'),
        ('accessory', 'Accessory'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)          # wajib
    price = models.IntegerField()                    # wajib
    description = models.TextField()                 # wajib
    thumbnail = models.URLField()                    # wajib
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES) # wajib
    is_featured = models.BooleanField(default=False) # wajib
