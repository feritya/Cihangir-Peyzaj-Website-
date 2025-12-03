from django.contrib import admin
from .models import ContactSettings, ContactMessage, Project, ProjectImage, OfferRequest

@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("created_at",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    inlines = [ProjectImageInline]

@admin.register(OfferRequest)
class OfferRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "service_type", "created_at")
    list_filter = ("service_type", "created_at")
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)