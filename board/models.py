from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.title
    
