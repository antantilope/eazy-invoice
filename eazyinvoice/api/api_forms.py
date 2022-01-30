
from django import forms


class NewHoursEntryForm(forms.Form):
    rate_id = forms.CharField(max_length=255)
    ord_id = forms.CharField(max_length=255)
    quantity = forms.DecimalField(min_value=0, decimal_places=2)
    date = forms.DateField()
    description = forms.CharField(
        max_length=1000,
        required=False,
        empty_value=None,
    )
