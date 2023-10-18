from django.contrib import admin
from .models import Unternehmen, Personal, Dokument
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


class DokumentInline(admin.TabularInline):
    model = Dokument
    extra = 0  # Anzahl der leeren Formulare, die standardmäßig angezeigt werden


def export_xlsx(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Personal'

    for col_num, column_title in enumerate(field_names, 1):
        col_letter = get_column_letter(col_num)
        ws['{}1'.format(col_letter)] = column_title

    for row_num, obj in enumerate(queryset, 2):
        for col_num, field in enumerate(field_names, 1):
            col_letter = get_column_letter(col_num)
            value = getattr(obj, field)
            if isinstance(value, Unternehmen):  # Replace `Unternehmen` with your actual model name
                value = value.location  # Replace `name` with the field you want to display
            ws['{}{}'.format(col_letter, row_num)] = value

    wb.save(response)

    return response


export_xlsx.short_description = "Ausgewählte Objekte als Excel exportieren"


class PersonalAdmin(admin.ModelAdmin):
    inlines = [DokumentInline]
    fieldsets = (
        ('Persönliche Informationen', {
            'fields': ('name', 'nachname', 'geburtsdatum', 'telefonnummer', 'email', 'email_passwort')
        }),
        ('Arbeitsdetails', {
            'fields': ('eintritt', 'austritt', 'status', 'vertragsart', 'standort')
        }),
        ('Finanzielle Informationen', {
            'fields': ('steuernummer', 'steuerklasse', 'sozialversicherungsnummer', 'iban')
        }),
        ('Weitere Informationen', {
            'fields': (
                'transportmittel', 'uberaccount', 'ubereats_passwort',
                'sign')
        }),
    )
    list_filter = ('standort__name', 'standort__location',)  # Filtern nach Unternehmen und Standort
    actions = [export_xlsx]
    list_display = ('name', 'status', 'standort')


from django.urls import reverse
from django.utils.html import format_html

class DokumentAdmin(admin.ModelAdmin):
    list_display = ('titel', 'personal', 'view_document')
    list_filter = ('personal__name',)

    def view_document(self, obj):
        url = obj.datei.url
        return format_html(f'<a href="{url}" target="_blank">Öffnen</a>')

admin.site.register(Dokument, DokumentAdmin)

admin.site.register(Unternehmen)
admin.site.register(Personal, PersonalAdmin)
