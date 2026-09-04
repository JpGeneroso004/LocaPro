from django import forms
from .models import Tenda, ConjuntoPalco


class TendaForm(forms.ModelForm):
    class Meta:
        model = Tenda
        # Código gerado automaticamente — não aparece no form
        fields = ['tamanho', 'tipo', 'status', 'observacoes']
        widgets = {
            'tamanho':    forms.Select(attrs={'class': 'form-control'}),
            'tipo':       forms.Select(attrs={'class': 'form-control'}),
            'status':     forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Ex: lona com rasgo pequeno...'}),
        }
        labels = {
            'tamanho': 'Tamanho',
            'tipo':    'Tipo',
            'status':  'Status',
            'observacoes': 'Observações (opcional)',
        }


class ConjuntoPalcoForm(forms.ModelForm):
    class Meta:
        model = ConjuntoPalco
        fields = ['nome', 'quantidade_placas', 'status', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Palco Principal, Piso Casamento...'
            }),
            'quantidade_placas': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '1', 'max': '30'
            }),
            'status':     forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Ex: algumas placas com borda desgastada...'
            }),
        }
        labels = {
            'nome':              'Nome do Conjunto',
            'quantidade_placas': 'Número de Placas (1–30)',
            'status':            'Status',
            'observacoes':       'Observações (opcional)',
        }
