from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from badge_site.models import Award, Issuer, Badge

class IndexView(TemplateView):
	template_name = 'index.html'


class IssuerCreateView(CreateView):
	model = Issuer
	template_name = 'create_view.html'

class BadgeCreateView(CreateView):
	model = Badge
	template_name = 'create_view.html'

class AwardCreateView(CreateView):
	model = Award
	template_name = 'create_view.html'






