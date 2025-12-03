from .models import ContactSettings

def global_settings(request):
    return {
        "global_settings": ContactSettings.objects.first()
    }
