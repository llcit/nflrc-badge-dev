import random, string, datetime

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from .models import Award, Issuer, Badge
from .forms import CreateIssuerForm, CreateBadgeForm, CreateAwardForm
from .mixins import ClassNameMixin


def getRandomDateSeedString(size=12, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	s = datetime.datetime.now().strftime('%Y%m%d')
	return s + ''.join(random.choice(chars) for x in range(size))

class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['badge_list'] = Badge.objects.all().order_by('created')
		return context


class IssuerCreateView(ClassNameMixin, CreateView):
	model = Issuer
	template_name = 'create_view.html'
	form_class = CreateIssuerForm
	success_url = reverse_lazy('home')
	object_name = 'Issuer'

	def get_initial(self):
		initial  = self.initial.copy()
		initial['guid'] = getRandomDateSeedString(size=2) 
		return initial

class IssuerUpdateView(ClassNameMixin, UpdateView):
	model = Issuer
	template_name = 'update_view.html'
	success_url = reverse_lazy('home')
	object_name = 'Issuer'
	fields = ['name', 'initials', 'url', 'doc_path', 'desc', 'image', 'contact']

class BadgeCreateView(ClassNameMixin, CreateView):
	model = Badge
	template_name = 'create_view.html'
	form_class = CreateBadgeForm
	success_url = reverse_lazy('home')
	object_name = 'Badge'

	def get_initial(self):
		initial  = self.initial.copy()
		initial['guid'] = getRandomDateSeedString(size=2) 
		return initial

class BadgeUpdateView(ClassNameMixin, UpdateView):
	model = Badge
	template_name = 'update_view.html'
	success_url = reverse_lazy('home')
	object_name = 'Badge'
	fields = ['name', 'image', 'description', 'criteria', 'issuer']


class AwardCreateView(ClassNameMixin, CreateView):
	model = Award
	template_name = 'create_view.html'
	form_class = CreateAwardForm
	success_url = reverse_lazy('home')
	object_name = 'Award'

	def get_initial(self):
		initial  = self.initial.copy()
		initial['guid'] = getRandomDateSeedString(size=2) 
		return initial


class AwardUpdateView(ClassNameMixin, UpdateView):
	model = Award
	template_name = 'update_view.html'
	success_url = reverse_lazy('home')
	object_name = 'Award'
	fields = ['email', 'firstname', 'lastname', 'badge', 'creator', 'evidence', 'expires']




