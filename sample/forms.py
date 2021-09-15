from django import forms
import datetime
from neighborhood.models import Neighborhood

# class SampleForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#          self.user = kwargs.pop('user', None)
#          super(SampleForm, self).__init__(*args, **kwargs)
#
#     neighborhood_list = Neighborhood.objects.filter(author=user.id)
#     nhood_choices = tuple(zip(neighborhood_list, [n.name for n in neighborhood_list]))
#
#     nhood = forms.ChoiceField(label='Neighborhood',required=True,help_text="Pick a Neighborhood from the dropdown menu",choices=nhood_choices)
#
#     num_points = forms.IntegerField(max_value=20,min_value=1,label='Number of Points',required=True)
#
#     critical_date = forms.DateField(initial=datetime.date.today)
