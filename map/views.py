from django.views.generic import FormView

from .forms import MapForm


class MapFormView(FormView):
    form_class = MapForm
    template_name = "map/map.html"
