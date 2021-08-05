import datetime
from django.forms import *


class DateInputP(DateInput):
    input_type = 'date'


class ReportForm(Form):
    usuario = CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    producto = CharField(required=True,
                         widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'name': 'product'}))
    date_start = DateField(required=True,
                           widget=DateInputP(attrs={'class': 'form-control', 'autocomplete': 'off',
                                                    'value': datetime.datetime.strftime(datetime.datetime(1999, 5, 17),
                                                                                        "%Y-%m-%d")}))
    date_end = DateField(required=True,
                         widget=DateInputP(
                             attrs={'class': 'form-control', 'autocomplete': 'off',
                                    'value': datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")}))


class FieldForm(Form):
    field = CharField(required=True, widget=TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))


class DateForm(Form):
    date = CharField(required=False, widget=TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
