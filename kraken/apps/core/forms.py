from django import forms
from django.forms import ModelForm, TextInput

from kraken.apps.core.models import Client, ClientSchema, SchemaVersion, VersionFile


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(error_messages={
            'required': 'Client Name field is required',
            'invalid': 'Client Name field is not a valid value'
        })
        self.fields['name'].widget = TextInput(attrs={
            'placeholder': 'Client Name',
            'class': 'form-control'
        })


class ClientSchemaForm(ModelForm):
    class Meta:
        model = ClientSchema
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientSchemaForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(error_messages={
            'required': 'Schema Name field is required',
            'invalid': 'Schema Name field is not a valid value'
        })
        self.fields['name'].widget = TextInput(attrs={
            'placeholder': 'Schema Name',
            'class': 'form-control'
        })


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


class VersionFileForm(ModelForm):
    class Meta:
        model = VersionFile
        exclude = ['schema_version']

    def __init__(self, *args, **kwargs):
        super(VersionFileForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(error_messages={
            'required': 'File Name field is required',
            'invalid': 'File Name field is not a valid value'
        })
        self.fields['name'].widget = TextInput(attrs={
            'placeholder': 'File Name',
            'class': 'form-control'
        })