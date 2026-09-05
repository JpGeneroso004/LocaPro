from django import forms
from .models import Equipamento, CategoriaEquipamento

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaEquipamento
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Iluminação'})
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['codigo', 'nome', 'categoria', 'quantidade_total', 'valor_diaria', 'status', 'observacoes']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-gerado se vazio'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cadeira Tiffany'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'valor_diaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O queryset será sobrescrito na view para filtrar pelo tenant
