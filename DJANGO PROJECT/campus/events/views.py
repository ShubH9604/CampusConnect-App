from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event, EventRegistration
from .forms import EventForm, EventRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
from .forms import EventRegistrationForm
# from django.core.mail import send_mail
# from django.http import HttpResponse

# Home page view
def home(request):
    events = Event.objects.filter(event_datetime__gte=timezone.now()).order_by('event_datetime')[:3]
    return render(request, 'home.html', {'events': events})

# Events page view
def events(request):
    # Fetch only approved events and order them by event date and time
    approved_events = Event.objects.filter(is_approved=True).order_by('event_datetime')

    # If no events are approved yet, you can display a message to the user
    if not approved_events:
        message = "No events have been approved yet."
    else:
        message = ""

    return render(request, 'events.html', {'events': approved_events, 'message': message})

# Send mail view
    # def send_test_email(request):
    #     send_mail(
    #         'Test Subject',
    #         'This is a test message',
    #         'shubh.kalaria@gmail.com',  # Sender's email
    #         ['recipient@example.com'],  # Receiver's email
    #         fail_silently=False,
    #     )
    #     return HttpResponse('Email sent successfully!')

# Event details view
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_registered = False

    if request.user.is_authenticated:
        user_registered = event.registrations.filter(user=request.user).exists()

    context = {
        'event': event,
        'registered': user_registered
    }
    return render(request, 'event_detail.html', context)


# Event register form view
def event_register(request, event_id):
    event = Event.objects.get(id=event_id)
    
    # Check if the user is already registered for the event
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.error(request, "You are already registered for this event.")
        return redirect('event_detail', event_id=event_id)
    
    if request.method == "POST":
        # Assuming you have a form to handle the registration
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, "You have successfully registered for the event!")
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventRegistrationForm()

    return render(request, 'event_register.html', {'form': form, 'event': event})

# Participation page view
@login_required
def participation(request):
    # Fetch the events the user has registered for
    participation = EventRegistration.objects.filter(user=request.user)

    # Pass the participation (events) to the template
    return render(request, 'participation.html', {'participation': participation})

# About page view
def about(request):
    return render(request, 'about.html')

# Create a new event
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

# Update an existing event
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:
        raise Http404("You are not allowed to edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'update_event.html', {'form': form})

# Delete an existing event
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:
        raise Http404("You are not allowed to delete this event.")

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('events')
    return render(request, 'delete_event.html', {'event': event})

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Log the user in
                auth_login(request, user)
                messages.success(request, "You have successfully logged in!")
                
                # Redirect to the next page (if available), or to the home page
                next_page = request.GET.get('next', 'home')  # Default to 'home' if no 'next' is present
                return redirect(next_page)
            else:
                # Invalid credentials
                messages.error(request, "Invalid username or password.")
        else:
            # Form is not valid
            messages.error(request, "Invalid username or password.")
    else:
        # GET request: display empty login form
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})