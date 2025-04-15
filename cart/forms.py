from django import forms

class DiscountForm(forms.Form):
    discount_code = forms.CharField(max_length=15)
