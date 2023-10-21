from django.contrib import admin
from .models import Unternehmen, Personal, Dokument
import csv
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import zipfile
from django.http import HttpResponse
from django.utils.html import format_html
import os
from datetime import datetime, timedelta


class DokumentInline(admin.TabularInline):
    model = Dokument
    extra = 0  # Anzahl der leeren Formulare, die standardmäßig angezeigt werden


def export_xlsx(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    # Manuell die Position von 'projekt' festlegen
    insert_index = field_names.index('standort') + 1
    field_names.insert(insert_index, 'projekt')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Personal'

    # Add headers
    for col_num, column_title in enumerate(field_names, 1):
        col_letter = get_column_letter(col_num)
        ws['{}1'.format(col_letter)] = column_title

    for row_num, obj in enumerate(queryset, 2):
        for col_num, field in enumerate(field_names, 1):
            col_letter = get_column_letter(col_num)
            if field == 'standort':
                value = obj.standort.standort  # Zugriff auf das 'standort'-Feld des 'Unternehmen'-Objekts
            elif field == 'projekt':
                value = obj.standort.projekt if obj.standort else None  # Zugriff auf das 'projekt'-Feld des 'Unternehmen'-Objekts
            else:
                value = getattr(obj, field)
            ws['{}{}'.format(col_letter, row_num)] = value

    wb.save(response)

    return response


export_xlsx.short_description = "Ausgewählte Objekte als Excel exportieren"


class PersonalAdmin(admin.ModelAdmin):
    inlines = [DokumentInline]
    fieldsets = (
        ('Persönliche Informationen', {
            'fields': ('name', 'nachname', 'personalnummer', 'geburtsdatum', 'telefonnummer', 'email', 'email_passwort')
        }),
        ('Arbeitsdetails', {
            'fields': ('eintritt', 'austritt', 'status', ('vertragsart', 'sign'), 'standort')
        }),
        ('Finanzielle Informationen', {
            'fields': ('steuernummer', 'steuerklasse', 'sozialversicherungsnummer', 'iban', 'finanziell_komplett')
        }),
        ('Weitere Informationen', {
            'fields': (
                'transportmittel', 'uberaccount', 'ubereats_passwort',
            )
        }),
    )
    list_filter = ('status', 'standort__projekt', 'standort__standort', 'finanziell_komplett')  # Aktualisierte Felder
    actions = [export_xlsx]
    list_display = (
        'name', 'nachname', 'personalnummer', 'status_colored', 'unternehmen_name', 'unternehmen_location',
        'vertragsende', 'probezeit_status',
        'finanziell_komplett_colored', 'sign_colored')

    def status_colored(self, obj):
        color = 'green' if obj.status == 'aktiv' else 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())

    status_colored.admin_order_field = 'status'  # Erlaubt das Sortieren
    status_colored.short_description = 'Status'  # Setzt die Spaltenüberschrift


    def sign_colored(self, obj):
        if obj.sign:
            color = 'green'
            text = 'check'
        else:
            color = 'red'
            text = 'uncheck'
        return format_html('<span style="color: {};">{}</span>', color, text)

    sign_colored.admin_order_field = 'sign'  # Erlaubt das Sortieren nach diesem Feld
    sign_colored.short_description = 'Sign'  # Setzt die Spaltenüberschrift

    def unternehmen_name(self, obj):
        return obj.standort.projekt if obj.standort else 'Nicht zugewiesen'

    unternehmen_name.admin_order_field = 'standort__projekt'  # Erlaubt das Sortieren
    unternehmen_name.short_description = 'Projekt'

    def unternehmen_location(self, obj):
        return obj.standort.standort if obj.standort else 'Nicht zugewiesen'

    unternehmen_location.admin_order_field = 'standort__standort'  # Erlaubt das Sortieren
    unternehmen_location.short_description = 'Standort'

    def finanziell_komplett_colored(self, obj):
        if obj.finanziell_komplett:
            color = 'green'
            text = 'check'
        else:
            color = 'red'
            text = 'uncheck'
        return format_html('<span style="color: {};">{}</span>', color, text)

    finanziell_komplett_colored.admin_order_field = 'finanziell_komplett'  # Erlaubt das Sortieren
    finanziell_komplett_colored.short_description = 'Finanz'  # Setzt die Spaltenüberschrift

    def vertragsende(self, obj):
        if obj.austritt:
            delta = obj.austritt - datetime.now().date()
            days_remaining = delta.days
            if days_remaining <= 0:
                color = 'red'
                text = f'abgelaufen seit {days_remaining} Tage'
            elif days_remaining <= 30:
                color = 'orange'
                text = f'in {days_remaining} Tage'
            else:
                color = 'green'
                text = f'in {days_remaining} Tage'
            return format_html('<span style="color: {};">{}</span>', color, text)
        return 'Austrittsdatum nicht festgelegt'

    def probezeit_status(self, obj):
        if obj.eintritt:
            probezeit_ende = obj.eintritt + timedelta(days=180)  # 6 Monate = 180 Tage
            delta = probezeit_ende - datetime.now().date()
            days_remaining = delta.days
            if days_remaining <= 0:
                color = 'white'
                text = 'beendet'
            elif days_remaining <= 30:
                color = 'orange'
                text = f'noch {days_remaining} Tage'
            else:
                color = 'green'
                text = f'noch {days_remaining}'
            return format_html('<span style="color: {};">{}</span>', color, text)
        return 'Eintrittsdatum nicht festgelegt'

    vertragsende.admin_order_field = 'austritt'
    vertragsende.short_description = 'Vertragsende'

    probezeit_status.admin_order_field = 'eintritt'
    probezeit_status.short_description = 'Probezeit'

    class Media:
        js = ('js/admin.js',)


from django.urls import reverse
from django.utils.html import format_html


def download_as_zip(modeladmin, request, queryset):
    zip_filename = 'Dokumente.zip'
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zipf:
        for doc in queryset:
            filename = os.path.basename(doc.datei.name)
            folder = f"{doc.personal.name}_{doc.personal.id}"
            zipf.write(doc.datei.path, os.path.join(folder, filename))

    return response


download_as_zip.short_description = "Ausgewählte Dokumente als ZIP herunterladen"


class DokumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'personal', 'view_document')
    list_filter = ('personal__name',)
    actions = [download_as_zip]  # Fügen Sie die Aktion hier hinzu

    def file_name(self, obj):
        return os.path.basename(obj.datei.name)

    def view_document(self, obj):
        url = obj.datei.url
        return format_html(f'<a href="{url}" target="_blank">Öffnen</a>')

    view_document.short_description = 'Dokument anzeigen'
    file_name.short_description = 'Dateiname'


admin.site.register(Dokument, DokumentAdmin)
admin.site.register(Unternehmen)
admin.site.register(Personal, PersonalAdmin)
