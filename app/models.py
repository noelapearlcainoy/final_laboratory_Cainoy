from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class LostItemReport(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Claimed', 'Claimed'),
    )

    CATEGORY_CHOICES = (
        ('ID', 'ID'),
        ('Gadget', 'Gadget'),
        ('Book', 'Book'),
        ('Wallet', 'Wallet'),
        ('Others', 'Others'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')
    description = models.TextField()
    date_found = models.DateField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"