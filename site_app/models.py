from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    product_id = models.UUIDField(primary_key=False, default=uuid.uuid4)
    price = models.FloatField()
    category = models.TextField()
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    buyer_address = models.TextField(null=True)
    is_bought = models.BooleanField()