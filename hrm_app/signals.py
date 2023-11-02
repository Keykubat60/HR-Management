import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Personal, Lohnprogramm

# Erstellen Sie einen Logger für Ihre Anwendung
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Personal)
def send_notification(sender, instance, created, **kwargs):
    # Überprüfen Sie, ob ein Lohnprogramm-Eintrag existiert, der das Personal als angemeldet markiert
    last_status = Lohnprogramm.objects.filter(personal=instance).last()

    if created:
        logger.info(
            f"Created: {created}, Gekündigt: {instance.gekuendigt}, Last Status: {last_status.status if last_status else 'Kein Status'}")

        # Wenn kein Lohnprogramm-Status vorhanden ist oder der letzte Status 'abgemeldet' ist
        if not last_status or last_status.status == 'abgemeldet':
            subject = 'Neuer Personal Eintrag'
            message = f"Hallo,\n\nEs wurde ein neuer Personal Eintrag gemacht. Wir bitten dich für die Anmeldung von {instance.name} {instance.nachname}.\n\nBitte vergiss nicht, die Datenbank als angemeldet zu aktualisieren.\n\nLG"
            send_email(subject, message)
    else:
        # Wenn das Personal gekündigt ist, aber der letzte Status nicht 'abgemeldet' ist
        if instance.gekuendigt and (not last_status or last_status.status == 'angemeldet'):
            logger.info(
                f"Created: {created}, Gekündigt: {instance.gekuendigt}, Last Status: {last_status.status if last_status else 'Kein Status'}")

            subject = 'Personal Gekündigt'
            message = f"Hallo,\n\nEs wurde ein Personal zum {instance.austritt} gekündigt. Wir bitten dich für die Abmeldung von {instance.name} {instance.nachname}.\n\nBitte vergiss nicht, die Datenbank als abgemeldet zu aktualisieren.\n\nLG"
            send_email(subject, message)

from django.contrib.auth.models import User

def send_email(subject, message):
    # Holen Sie alle Benutzer, die als Staff gekennzeichnet sind und eine E-Mail-Adresse haben
    staff_users_with_email = User.objects.filter(
        is_staff=True,
        email__isnull=False  # Stellen Sie sicher, dass der Benutzer eine E-Mail-Adresse hat
    ).distinct()

    # Erstellen Sie eine Liste von E-Mail-Adressen
    email_list = list(staff_users_with_email.values_list('email', flat=True))

    # Senden Sie die E-Mail
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        email_list,
        fail_silently=False,
    )


# Verbinden Sie das Signal mit dem Modell Personal
post_save.connect(send_notification, sender=Personal)
