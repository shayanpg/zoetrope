from django import forms

class SampleForm(forms.Form):
    nhood = forms.CharField(label='Street Address',
     help_text="Pick a Neighborhood from the dropdown menu")
