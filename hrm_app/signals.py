from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Personal
@receiver(post_save, sender=Personal)
def send_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'Neuer Personal Eintrag'
        message = f"Hallo,\n\nEs wurde ein neuer Personal Eintrag gemacht. Wir bitten dich für die Anmeldung von {instance.name} {instance.nachname}.\n\nBitte vergiss nicht, die Datenbank als angemeldet zu aktualisieren.\n\nLG"
        print("created")
    else:
        if instance.gekuendigt:
            subject = 'Personal Gekündigt'
            message = f"Hallo,\n\nEs wurde ein Personal zu {instance.austritt} gekündigt. Wir bitten dich für die Abmeldung von {instance.name} {instance.nachname}.\n\nBitte vergiss nicht, die Datenbank als abgemeldet zu aktualisieren.\n\nLG"
            print("gekündigt")
        else:
            print("leer")

            return  # Keine Aktion erforderlich, wenn nicht gekündigt

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['tuerkboy97@gmail.com'],  # Die E-Mail-Adresse des Beauftragten
        fail_silently=False,
    )

# Verbinden Sie das Signal mit dem Modell Personal
post_save.connect(send_notification, sender=Personal)