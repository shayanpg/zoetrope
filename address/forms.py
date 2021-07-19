from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(label='Street Address',
     help_text="e.g. 2155 Center St, Berkeley, CA 94720",
     max_length=100)
