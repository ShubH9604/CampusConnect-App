from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='event_photos/', blank=True, null=True)
    organized_by = models.CharField(max_length=100, default="Unknown")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} organized by {self.organized_by} on {self.event_datetime.strftime('%Y-%m-%d %H:%M')}"

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

