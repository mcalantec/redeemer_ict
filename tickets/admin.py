from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Ticket, TicketComment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'title', 'category', 'priority', 'status', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'category', 'priority', 'created_at']
    search_fields = ['ticket_id', 'title', 'description']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    list_filter = ['created_at']