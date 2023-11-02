# forms.py (erstellen Sie diese Datei in Ihrer App, falls noch nicht vorhanden)

from django import forms
from django.forms import inlineformset_factory
from .models import Personal, Kind

# Formular für das Personal-Modell
class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = '__all__'

# Formular für das Kind-Modell
class KindForm(forms.ModelForm):
    class Meta:
        model = Kind
        fields = ('name', 'geburtsdatum',)

# Formset für Kinder
KindFormSet = inlineformset_factory(
    Personal, Kind, form=KindForm,
    fields=('name', 'geburtsdatum',), extra=1, can_delete=True
)

class CustomDatePickerWidget(forms.DateInput):
    input_type = 'text'  # Ändern Sie den Typ zu 'text', um das Format zu erzwingen
    format = '%d.%m.%Y'
