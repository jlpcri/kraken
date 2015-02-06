from django import forms
from django.forms import ModelForm, TextInput

from kraken.apps.core.models import Client, ClientSchema


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