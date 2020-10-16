from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budget", null=True)
    name = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    budget = models.ForeignKey(Budget, on_delete = models.CASCADE)
    text = models.CharField(max_length = 300)
    cost = models.CharField(max_length = 300, null=True)
    
    def __str__(self):
        return self.text    