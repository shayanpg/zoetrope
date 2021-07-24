from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(label='Street Address',
     help_text="e.g. 2384 Telegraph Ave, Berkeley, CA 94704",
     max_length=100)
