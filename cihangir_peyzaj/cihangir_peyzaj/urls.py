"""
URL configuration for cihangir_peyzaj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from main.models import Project
from django.views.generic import TemplateView

class StaticViewSitemap(Sitemap):
    priority = 0.9  
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'services', 'contact']

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),  
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact_view, name='contact'),


    path('services/peyzaj-tasarim/', views.services_tasarim, name='peyzaj_tasarim'), 
    path('services/sulama/',views.services_sulama, name='sulama'),
    path('services/cim-serimi/',views.services_cim, name='cim_serimi'),
    path('services/bitkilendirme/',views.services_bitkilendirme,name='bitkilendirme'),
    path('services/sert-zemin/',views.services_sert_zemin,name='sert_zemin'),
    path('services/villa-bakim/',views.services_villa_bakim,name='villa_bakim'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('teklif-al/', views.offer_view, name="offer"),

    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path('sitemap.xml', sitemap, {
        'sitemaps': {
            'static': StaticViewSitemap(),
            'projects': ProjectSitemap(),
        }
    }),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'main.views.custom_404'
