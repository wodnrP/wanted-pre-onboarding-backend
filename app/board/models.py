from django.db import models
from user.models import User

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)
    user = models.ForeignKey("user.User", related_name='+', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
