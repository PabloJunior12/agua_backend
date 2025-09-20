import datetime
import django_filters
import pandas as pd

from datetime import date
from decimal import Decimal, InvalidOperation
from .models import Reading, Debt

MESES = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SETIEMBRE": 9,
    "SEPTIEMBRE": 9,  # por si acaso
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12,
}


def next_month_date(date_obj):
    """Devuelve la fecha correspondiente al siguiente mes, con día=1."""
    year = date_obj.year
    month = date_obj.month + 1
    if month > 12:
        month = 1
        year += 1
    # Si tus lecturas siempre se guardan con day=1, puedes forzarlo a 1:
    return datetime.date(year, month, 1)

def flatten_errors(error_dict):
    """
    Convierte errores del serializer en un string plano legible.
    Compatible con errores anidados.
    """
    if isinstance(error_dict, dict):
        messages = []
        for field, errors in error_dict.items():
            if isinstance(errors, list):
                for error in errors:
                    messages.append(f"{field}: {error}")
            elif isinstance(errors, dict):
                nested = flatten_errors(errors)
                messages.append(f"{field}: {nested}")
            else:
                messages.append(f"{field}: {errors}")
        return ' | '.join(messages)
    elif isinstance(error_dict, list):
        return ' | '.join(str(e) for e in error_dict)
    return str(error_dict)

class ReadingFilter(django_filters.FilterSet):

    year = django_filters.NumberFilter(field_name='period', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='period', lookup_expr='month')

    class Meta:
        
        model = Reading
        fields = ['customer', 'paid', 'year', 'month']

class DebtFilter(django_filters.FilterSet):

    year = django_filters.NumberFilter(field_name='period', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='period', lookup_expr='month')

    class Meta:
        
        model = Debt
        fields = ['customer', 'paid', 'year', 'month', 'customer__codigo']

def to_none_if_empty(value):
    """
    Convierte el valor a None si está vacío, es NaN o solo contiene espacios.
    Caso contrario, devuelve el string sin espacios.
    """
    if pd.isna(value):  # Detecta NaN de pandas
        return None
    value_str = str(value).strip()
    return value_str if value_str else None

def to_decimal_or_none(value):
    """
    Convierte un valor a Decimal si es posible, 
    o devuelve None si está vacío, es NaN o no es convertible.
    """
    if value is None:
        return None
    if str(value).strip() == "" or str(value).strip().lower() == "nan":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    
def generar_periodos(anio, meses_texto):

    """
    meses_texto: "DE ENERO A DICIEMBRE" o "DE JULIO A DICIEMBRE"
    """
    partes = meses_texto.replace("DE ", "").split(" A ")
    mes_inicio = MESES[partes[0].strip().upper()]
    mes_fin = MESES[partes[1].strip().upper()]

    periodos = []
    for mes in range(mes_inicio, mes_fin + 1):
        periodos.append(date(anio, mes, 1))
    return periodos