from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm
from .models import ContactSettings, ContactMessage, Project, OfferRequest
import time


# Create your views here.


def index(request):
    featured_projects = Project.objects.order_by('created_at')[:3]  # son eklenen 3 proje

    context = {
        "featured_projects": featured_projects
    }
    return render(request, "index.html", context )

def about(request):
    return render(request, 'about.html')    
def services(request):
    return render(request, 'service.html')


def services_tasarim(request):
    return render(request, 'services/peyzaj_tasarim.html')
def services_sulama(request):
    return render(request, 'services/sulama.html')

def services_cim(request):
    return render(request, 'services/cim.html')

def services_bitkilendirme(request):
    return render(request, 'services/bitkilendirme.html')
def services_sert_zemin(request):
    return(render(request, 'services/sert_zemin.html'))
def services_villa_bakim(request):
    return(render(request, 'services/villa_bakim.html'))



def contact_view(request):
    settings_data = ContactSettings.objects.first()
    form = ContactForm()

    if request.method == "POST":
                # 🔐 Honeypot kontrolü (bot doldurursa yakalanır)
        if request.POST.get("website"):
            messages.error(request, "Form gönderilemedi.")
            return redirect("contact")

        # 🔐 Zaman koruması (bot çok hızlı gönderir)
        try:
            start = float(request.POST.get("timestamp"))
            if time.time() - start < 2:  # 2 saniyeden hızlı dolduran bot
                messages.error(request, "Form gönderilemedi.")
                return redirect("contact")
        except:
            pass
        
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
            )

            email_body = f"""
Gönderen: {name}
Email: {email}


Mesaj:
{message}
"""

            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings_data.email],  # şirket maili
                    fail_silently=False
                )
                messages.success(request, "Mesajınız başarıyla gönderildi. Teşekkür ederiz!")
                return redirect("contact")

            except Exception as e:
                messages.error(request, "Mesaj gönderilirken hata oluştu. Lütfen tekrar deneyin.")

    return render(request, "contact.html", {
        "form": form,
        "settings": settings_data,
        "timestamp": time.time(), 

    })

def projects(request):
    projects = Project.objects.all()
    return render(request, "project.html", {"projects": projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_detail.html", {"project": project})






def offer_view(request):
    if request.method == "POST":
                # Honeypot
        if request.POST.get("website"):
            return redirect("offer")

        # Anti-bot timer
        try:
            start = float(request.POST.get("timestamp"))
            if time.time() - start < 2:
                return redirect("offer")
        except:
            pass

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        service_type = request.POST.get("service_type")
        message = request.POST.get("message")

        # 1) Admin'e kaydet
        offer = OfferRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            service_type=service_type,
            message=message
        )

        # 2) Mail gönder
        email_body = f"""
Yeni Teklif Talebi

Ad Soyad: {name}
Telefon: {phone}
Email: {email}
Hizmet Türü: {service_type}

Mesaj:
{message}

Gönderim Tarihi: {offer.created_at}
"""

        try:
            send_mail(
                subject=f"Yeni Teklif Talebi - {name}",
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["firma_mail_adresi@site.com"],  # gerçek firma maili
                fail_silently=False,
            )
            messages.success(request, "Talebiniz başarıyla iletildi. En kısa sürede size dönüş yapılacaktır.")
        except:
            messages.error(request, "Talep kaydedildi ancak mail gönderilemedi. Lütfen tekrar deneyin.")

    return render(request, "offer.html",{
        "timestamp": time.time(),
    })

def custom_404(request, exception):
    return render(request, '404.html', status=404)