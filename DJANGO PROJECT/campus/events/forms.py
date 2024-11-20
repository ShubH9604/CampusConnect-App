from django import forms
from .models import Event, EventRegistration
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Event creation form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_datetime', 'location', 'organized_by', 'photo']
        widgets = {
            'event_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def save(self, commit=True):
        event = super().save(commit=False)
        event.is_approved = False  # Set the default approval status to False
        if commit:
            event.save()
            self.notify_superuser(event)  # Notify superusers after saving
        return event

    @staticmethod
    def notify_superuser(event):
        superusers = User.objects.filter(is_superuser=True)
        emails = [user.email for user in superusers if user.email]  # Ensure superusers have an email
        if emails:  # Send email only if there are valid recipient emails
            send_mail(
                subject="New Event Awaiting Approval",
                message=f"The event '{event.title}' has been submitted for approval.",
                from_email="your_email@example.com",  # Replace with your email
                recipient_list=emails,
            )

# Event registration form
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone']