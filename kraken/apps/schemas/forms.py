from django import forms
from django.forms import ModelForm, TextInput

from kraken.apps.schemas.models import SchemaVersion


class SchemaVersionForm(ModelForm):
    class Meta:
        model = SchemaVersion
        exclude = ['client_schema', 'current']

    def __init__(self, *args, **kwargs):
        super(SchemaVersionForm, self).__init__(*args, **kwargs)
        self.fields['identifier'] = forms.CharField(error_messages={
            'required': 'Version Name field is required',
            'invalid': 'Version Name field is not a valid value'
        })
        self.fields['identifier'].widget = TextInput(attrs={
            'placeholder': '1.0',
            'class': 'form-control'
        })
        self.fields['delimiter'] = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=SchemaVersion.DELIMITER_TYPE_CHOICES
        )
