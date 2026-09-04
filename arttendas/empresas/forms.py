from django import forms
from .models import Organizacao

class OrganizacaoForm(forms.ModelForm):
    class Meta:
        model = Organizacao
        fields = ['nome', 'cnpj', 'telefone', 'logo', 'cor_primaria', 'clausulas_padrao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'cor_primaria': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'style': 'max-width: 100px;'}),
            'clausulas_padrao': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }
