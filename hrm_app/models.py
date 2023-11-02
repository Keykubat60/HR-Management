from django.db import models
import os
from django.db.models import UniqueConstraint
from datetime import datetime


# Unternehmen und Standort
class Unternehmen(models.Model):
    UNTERNEHMEN_CHOICES = [
        ('Hermes', 'Hermes'),
        ('Uber Eats', 'Uber Eats'),
    ]
    projekt = models.CharField(max_length=100, choices=UNTERNEHMEN_CHOICES)
    standort = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.projekt} - {self.standort}"
    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekte"

class Personal(models.Model):
    STATUS_CHOICES = [
        ('', '---'),  # Standardwert, nicht ausgewählt
        ('aktiv', 'Aktiv'),
        ('inaktiv', 'Inaktiv'),
    ]
    VERTRAGSART_CHOICES = [
        ('', '---'),  # Standardwert, nicht ausgewählt
        ('150€', '150€'),
        ('520€', '520€'),
        ('Teilzeit', 'Teilzeit'),
        ('Vollzeit', 'Vollzeit'),
    ]
    TRANSPORTMITTEL_CHOICES = [
        ('', '---'),  # Standardwert, nicht ausgewählt
        ('Auto', 'Auto'),
        ('Fahrrad', 'Fahrrad'),
    ]
    staatsbuergerschaft = models.CharField(max_length=100, null=True, blank=True, verbose_name='Staatsbürgerschaft')
    personalnummer = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100, null=True, blank=True)
    steuernummer = models.CharField(max_length=20, null=True, blank=True)
    steuerklasse = models.IntegerField(null=True, blank=True)
    iban = models.CharField(max_length=34, null=True, blank=True)
    geburtsdatum = models.DateField(null=True, blank=True)
    finanziell_komplett = models.BooleanField(default=False, verbose_name='Finanziell komplett')
    eintritt = models.DateField(null=True, blank=True)
    austritt = models.DateField(null=True, blank=True)
    sozialversicherungsnummer = models.CharField(max_length=50, verbose_name='SV-Nummer', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_passwort = models.CharField(max_length=100, null=True, blank=True)
    transportmittel = models.CharField(
        max_length=50,
        choices=TRANSPORTMITTEL_CHOICES,
        null=True,
        blank=True
    )
    telefonnummer = models.CharField(max_length=15, null=True, blank=True)
    ubereats_passwort = models.CharField(max_length=100, null=True, blank=True)
    standort = models.ForeignKey(Unternehmen, related_name='mitarbeiter', on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name='Projekt/Standort')
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='',
        null=True,
        blank=True
    )
    vertragsart = models.CharField(
        max_length=50,
        choices=VERTRAGSART_CHOICES,
        default='',
        null=True,
        blank=True
    )
    sign = models.BooleanField(default=False)
    uberaccount = models.CharField(max_length=100, null=True, blank=True)

    # Neue Felder hinzufügen
    strasse = models.CharField(max_length=255, null=True, blank=True)
    postleitzahl = models.CharField(max_length=10, null=True, blank=True)
    ort = models.CharField(max_length=100, null=True, blank=True)
    familienstand = models.CharField(
        max_length=20,
        choices=[
            ('ledig', 'Ledig'),
            ('verheiratet', 'Verheiratet'),
            ('geschieden', 'Geschieden'),
        ],
        null=True,
        blank=True
    )
    gekuendigt = models.BooleanField(default=False,verbose_name='gekündigt')
    lp_abgemeldet = models.BooleanField(default=False, verbose_name='LP abgemeldet')
    lp_angemeldet = models.BooleanField(default=False, verbose_name='LP angemeldet')
    krankenkassenname = models.CharField(max_length=255, null=True, blank=True)
    kinderfreibetrag = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Mitarbeiter"
        verbose_name_plural = "Mitarbeiter"

# Dokumente
def get_upload_to(instance, filename):
    return os.path.join('dokumente', f"{instance.personal.name}_{instance.personal.id}", filename)


class Dokument(models.Model):
    titel = models.CharField(max_length=100)
    datei = models.FileField(upload_to=get_upload_to)
    personal = models.ForeignKey(Personal, related_name='dokumente', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.datei:
            # Ändern Sie den Dateinamen in den Titel des Dokuments
            extension = os.path.splitext(self.datei.name)[1]
            self.datei.name = f"{self.titel}{extension}"
        super(Dokument, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Löschen Sie die physische Datei, bevor das Objekt gelöscht wird
        if self.datei:
            if os.path.isfile(self.datei.path):
                os.remove(self.datei.path)
        super(Dokument, self).delete(*args, **kwargs)

    def __str__(self):
        return self.titel
    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumente"
class Kind(models.Model):
    personal = models.ForeignKey(Personal, related_name='kinder', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    geburtsdatum = models.DateField()

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Kinder von Mitarbeiter"
        verbose_name_plural = "Kinder von Mitarbeiter"
class Monatsabrechnung(models.Model):
    MONAT_CHOICES = [
        ('Januar', 'Januar'),
        ('Februar', 'Februar'),
        ('März', 'März'),
        ('April', 'April'),
        ('Mai', 'Mai'),
        ('Juni', 'Juni'),
        ('Juli', 'Juli'),
        ('August', 'August'),
        ('September', 'September'),
        ('Oktober', 'Oktober'),
        ('November', 'November'),
        ('Dezember', 'Dezember'),
    ]

    monat = models.CharField(max_length=20, choices=MONAT_CHOICES)
    jahr = models.CharField(max_length=4)
    personal = models.ManyToManyField(
        Personal,
        through='Abrechnung',
        through_fields=('monatsabrechnung', 'personal'),
    )

    def __str__(self):
        return f"{self.monat} {self.jahr}"
    class Meta:
        verbose_name = "Abrechnungsmonat"
        verbose_name_plural = "Abrechnungsmonate"

class Abrechnung(models.Model):
    monatsabrechnung = models.ForeignKey(Monatsabrechnung, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    betrag = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ueberwiesen = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bar = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('monatsabrechnung', 'personal',)
        verbose_name = "Abrechnung"
        verbose_name_plural = "Abrechnungen"
    def __str__(self):
        return f"Abrechnung für {self.personal.name} für {self.monatsabrechnung}"

class Lohnprogramm(models.Model):
    STATUS_CHOICES = [
        ('angemeldet', 'angemeldet'),
        ('abgemeldet', 'abgemeldet'),
    ]
    personal = models.ForeignKey(Personal, related_name='anmeldestatus', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    datum = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_status_display()} am {self.datum.strftime('%d.%m.%Y')}"

    class Meta:
        # Optional: Definieren Sie eine Regel, dass nur der neueste Status als aktuell betrachtet wird
        get_latest_by = 'datum'
        verbose_name = "Lohnprogrammstatus"
        verbose_name_plural = "Lohnprogrammstatus"

