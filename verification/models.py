from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return self.name

class IDCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=50)
    scanned_image = models.ImageField(upload_to='scans/')
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.name}'s ID"


