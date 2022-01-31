
from django import forms

from api.models import Organization


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


class RunQueryForm(forms.Form):
    organizations = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all()
    )
    invoice_paid_start_date = forms.DateField(
        required=False,
    )
    invoice_paid_end_date = forms.DateField(
        required=False,
    )
    is_paid = forms.BooleanField(required=False)
