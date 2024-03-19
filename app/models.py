from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')

    def __str__(self):
        return f'Profile for {self.user.username}'




class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
    ]
    
    task_name = models.CharField(max_length=100)
    task_date = models.DateField()
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='Pending')
    task_info = models.TextField()
    task_comment = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)  # New field to store the order

    def __str__(self):
        return self.task_name
