from django import forms
from django.db import models as django_models
from .models import Evento
from .fields import DataBRField
from inventario.models import Tenda, ConjuntoPalco


class EventoForm(forms.ModelForm):
    tendas = forms.ModelMultipleChoiceField(
        queryset=Tenda.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'}),
        label='Tendas'
    )
    conjuntos = forms.ModelMultipleChoiceField(
        queryset=ConjuntoPalco.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
        label='Conjuntos de Palco/Piso'
    )
    data_inicio = DataBRField(label='Data de Início')
    data_fim    = DataBRField(label='Data de Fim')

    class Meta:
        model = Evento
        fields = ['nome', 'cliente', 'telefone', 'rua', 'numero', 'setor', 'complemento', 'cidade',
                  'data_inicio', 'hora_inicio', 'data_fim', 'hora_fim', 'status', 'observacoes', 'tendas', 'conjuntos']
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

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.fields['tendas'].queryset = Tenda.objects.filter(status='ativo').order_by('tamanho', 'tipo', 'codigo')
        self.fields['conjuntos'].queryset = ConjuntoPalco.objects.filter(status='ativo')

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim    = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error('data_fim', 'A data de fim não pode ser anterior à data de início.')

        # Validação detalhada de equipamentos será feita na view para suporte à regra de 24h e transições.
        return cleaned_data
