from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, TextInput

from kraken.apps.core.models import Client, ClientSchema, SchemaVersion, VersionFile


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(error_messages={
            'required': 'Client Name is required',
            'invalid': 'Client Name is not a valid value',
            'unique': 'Client Name already exists'
        })
        self.fields['name'].widget = TextInput(attrs={
            'placeholder': 'Client Name',
            'class': 'form-control'
        })


class ClientSchemaForm(ModelForm):
    class Meta:
        model = ClientSchema
        exclude = []
        error_messages = {
            NON_FIELD_ERRORS: {
                # 'unique_together': "%(model_name)s's %(field_labels)s are not unique",
                'unique_together': "Schema Name is not unique",
            }
        }

    def __init__(self, *args, **kwargs):
        super(ClientSchemaForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(error_messages={
            'required': 'Schema Name is required',
            'invalid': 'Schema Name is not a valid value'
        })
        self.fields['name'].widget = TextInput(attrs={
            'placeholder': 'Schema Name',
            'class': 'form-control'
        })


class SchemaVersionForm(ModelForm):
    class Meta:
        model = SchemaVersion
        exclude = ['client_schema', 'current']
        error_messages = {
            NON_FIELD_ERRORS: {
                # 'unique_together': "%(model_name)s's %(field_labels)s are not unique",
                'unique_together': "Version is not unique",
            }
        }

    def __init__(self, *args, **kwargs):
        super(SchemaVersionForm, self).__init__(*args, **kwargs)
        self.fields['identifier'] = forms.CharField(error_messages={
            'required': 'Version is required',
            'invalid': 'Version is not a valid value'
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
        exclude = ['schema_version', 'last_opened', 'contents']

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