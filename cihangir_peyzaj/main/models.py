from django.db import models


class ContactSettings(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    map_iframe = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "İletişim Ayarı"
        verbose_name_plural = "İletişim Ayarları"

    def __str__(self):
        return "Site İletişim Ayarları"
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Project(models.Model):
    STATUS_CHOICES = (
        ('finished', 'Tamamlanan Proje'),
        ('ongoing', 'Devam Eden Proje')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    cover_image = models.ImageField(upload_to="projects/cover/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")

    def __str__(self):
        return f"{self.project.title} Fotoğrafı"



class OfferRequest(models.Model):
    SERVICE_CHOICES = [
        ("Çim Serimi", "Çim Serimi"),
        ("Villa / Site Peyzajı", "Villa / Site Peyzajı"),
        ("Ağaç Ve Çalıların Dikimi", "Ağaç Ve Çalıların Dikimi"),
        ("Otomatik Sulama & Drenaj ", "Otomatik Sulama & Drenaj"),
        ("Sert Zemin & Yapısal Peyzaj", "Sert Zemin & Yapısal Peyzaj"),
        ("Peyzaj Tasarım ve Uygulamaları", "Peyzaj Tasarım ve Uygulamaları"),
        ("Toprak Dolgusu ", "Toprak Dolgusu"),
        ("Diğer", "Diğer"),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"
