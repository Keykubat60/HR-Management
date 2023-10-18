from django.db import models
import os
# Unternehmen und Standort
class Unternehmen(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.location

class Personal(models.Model):
    name = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100, null=True, blank=True)
    steuernummer = models.CharField(max_length=20, null=True, blank=True)
    steuerklasse = models.IntegerField(null=True, blank=True)
    iban = models.CharField(max_length=34, null=True, blank=True)
    geburtsdatum = models.DateField(null=True, blank=True)
    eintritt = models.DateField(null=True, blank=True)
    austritt = models.DateField(null=True, blank=True)
    sozialversicherungsnummer = models.CharField(max_length=50, verbose_name='SV-Nummer', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_passwort = models.CharField(max_length=100, null=True, blank=True)
    transportmittel = models.CharField(max_length=50, null=True, blank=True)
    telefonnummer = models.CharField(max_length=15, null=True, blank=True)
    ubereats_passwort = models.CharField(max_length=100, null=True, blank=True)
    standort = models.ForeignKey(Unternehmen, related_name='mitarbeiter', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    vertragsart = models.CharField(max_length=50, null=True, blank=True)
    sign = models.CharField(max_length=100, null=True, blank=True)
    uberaccount = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
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



