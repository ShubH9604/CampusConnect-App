from django.contrib import admin
from .models import Event, EventRegistration
from django.utils.html import mark_safe

# EventAdmin: Customize the Event model in the admin interface
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_datetime', 'location', 'organized_by', 'is_approved', 'photo_preview')
    list_filter = ('event_datetime', 'location', 'organized_by', 'is_approved')  # Added filter for approval status
    search_fields = ('title', 'location', 'organized_by')  # Searchable fields
    actions = ['approve_events', 'reject_events']  # Add custom admin actions

    # Show image in the admin list
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50"/>')
        return "No Image"
    photo_preview.short_description = 'Event Photo'

    # Action to approve events
    @admin.action(description='Approve selected events')
    def approve_events(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} event(s) approved successfully.")

    # Action to reject events
    @admin.action(description='Reject selected events')
    def reject_events(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} event(s) rejected and deleted successfully.")

# EventRegistrationAdmin: Customize the EventRegistration model in the admin interface
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'name', 'email', 'phone', 'registered_at')  # Display registration details
    list_filter = ('event',)  # Filter by event
    search_fields = ('user__username', 'event__title')  # Search by user and event title
    readonly_fields = ('user', 'event')  # Keep event and user fields read-only

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion of event registrations in the admin interface

# Register the models with the admin site
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
