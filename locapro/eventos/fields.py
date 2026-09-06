"""
Campo de data customizado: três caixinhas (Dia / Mês / Ano)
com avanço automático de foco, em vez do input nativo
type="date" (que fica com o segmento azul ao editar).
"""
from django import forms
from datetime import date


class DataBRWidget(forms.MultiWidget):
    """Renderiza três <input> — dia, mês, ano."""

    template_name = 'widgets/data_br.html'

    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={
                'class': 'form-control text-center mx-1 px-1',
                'placeholder': 'DD',
                'maxlength': '2',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'style': 'max-width: 60px; display: inline-block;'
            }),
            forms.TextInput(attrs={
                'class': 'form-control text-center mx-1 px-1',
                'placeholder': 'MM',
                'maxlength': '2',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'style': 'max-width: 60px; display: inline-block;'
            }),
            forms.TextInput(attrs={
                'class': 'form-control text-center mx-1 px-1',
                'placeholder': 'AAAA',
                'maxlength': '4',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'style': 'max-width: 80px; display: inline-block;'
            }),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                return value
            try:
                return [f'{value.day:02d}', f'{value.month:02d}', f'{value.year:04d}']
            except AttributeError:
                return [None, None, None]
        return [None, None, None]


class DataBRField(forms.Field):
    """
    Campo simples (não MultiValueField) que recebe a lista
    [dia, mes, ano] vinda do DataBRWidget e converte para um
    objeto date do Python.
    """
    widget = DataBRWidget

    default_error_messages = {
        'incompleto': 'Preencha dia, mês e ano.',
        'invalido': 'Data inválida. Verifique dia, mês e ano.',
    }

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, date):
            return value

        # value vem como lista: [dia, mes, ano]
        partes = list(value) + [None, None, None]
        dia, mes, ano = partes[0], partes[1], partes[2]

        dia = (dia or '').strip()
        mes = (mes or '').strip()
        ano = (ano or '').strip()

        if not dia and not mes and not ano:
            return None

        if not (dia and mes and ano):
            raise forms.ValidationError(self.error_messages['incompleto'], code='incompleto')

        try:
            return date(int(ano), int(mes), int(dia))
        except (ValueError, TypeError):
            raise forms.ValidationError(self.error_messages['invalido'], code='invalido')

    def validate(self, value):
        super().validate(value)
