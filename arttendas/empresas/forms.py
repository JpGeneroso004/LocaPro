from django import forms
from .models import Organizacao

class OrganizacaoForm(forms.ModelForm):
    class Meta:
        model = Organizacao
        fields = ['nome', 'cnpj', 'telefone', 'cidade', 'estado', 'pais', 'moeda', 'logo', 'cor_primaria', 'clausulas_padrao', 'fidelidade_ativa', 'pontos_por_real', 'taxa_resgate']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Miami, Lisboa, São Paulo'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: FL, SP'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: USA, Brasil'}),
            'moeda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: USD, BRL, EUR'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'cor_primaria': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'style': 'max-width: 100px;'}),
            'clausulas_padrao': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'fidelidade_ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pontos_por_real': forms.NumberInput(attrs={'class': 'form-control'}),
            'taxa_resgate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
