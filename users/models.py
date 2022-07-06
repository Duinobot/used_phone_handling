from django.contrib.auth.models import AbstractUser
from django.db import models
from phones.models import Location

# Create your models here.
class CustomUser(AbstractUser):
    Location = [
    ('Warehouse', 'Warehouse'),
    ('Repairs', 'Repairs'),
    ('Sold', 'Sold'),
    ]
    location = models.CharField(max_length=10,choices=Location, default='Repairs')
    company = models.CharField(max_length=20, null=True)