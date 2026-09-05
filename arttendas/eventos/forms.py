from django import forms
from django.db import models as django_models
from .models import Evento
from .fields import DataBRField


class EventoForm(forms.ModelForm):
    data_inicio = DataBRField(label='Data de Início')
    data_fim    = DataBRField(label='Data de Fim')

    class Meta:
        model = Evento
        fields = ['nome', 'cliente', 'telefone', 'rua', 'numero', 'setor', 'complemento', 'cidade',
                  'data_inicio', 'hora_inicio', 'data_fim', 'hora_fim', 'status', 'observacoes']
        widgets = {
            'nome':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do evento'}),
            'cliente':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente', 'id': 'input-cliente'}),
            'telefone':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(61) 99999-9999', 'id': 'input-telefone'}),
            'rua':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rua 10', 'id': 'input-rua'}),
            'numero':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123 ou S/N', 'id': 'input-numero'}),
            'setor':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Setor Sul', 'id': 'input-setor'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Perto do mercado', 'id': 'input-complemento'}),
            'cidade':    forms.TextInput(attrs={'class': 'form-control', 'id': 'input-cidade'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim':    forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status':      forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim    = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error('data_fim', 'A data de fim não pode ser anterior à data de início.')

        return cleaned_data
