

from django import forms
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect



from .models import Award, Issuer, Badge, Revocation
from .forms import CreateIssuerForm, CreateBadgeForm, CreateAwardForm, ClaimCodeSubmitForm, RevokeAwardForm
from .mixins import ClassNameMixin


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['issuer_list'] = Issuer.objects.all()
        context['badge_list'] = Badge.objects.all().order_by('created')
        return context


class BadgeClaimView(FormView):
    template_name = 'claim_view.html'
    form_class = ClaimCodeSubmitForm

    def get_success_url(self):
        return reverse('claim_badge_with_code', args=[self.claim_code])

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.claim_code = form.cleaned_data['claim_code'].strip()
        
        return HttpResponseRedirect(self.get_success_url())

        def get_context_data(self, **kwargs):
            context = super(BadgeClaimView, self).get_context_data(**kwargs)
            return context

class BadgeClaimCodeView(TemplateView):
    template_name = 'claim_view.html'
    
    def get_context_data(self, **kwargs):
        context = super(BadgeClaimCodeView, self).get_context_data(**kwargs)
        code = self.kwargs['claim_code']
        context['award'] = Award.objects.get(claimCode = code)
        return context



class IssuerListView(ClassNameMixin, ListView):
    model = Issuer
    template_name = 'list_view.html'
    class_name = 'Issuer'


class IssuerCreateView(ClassNameMixin, CreateView):
    model = Issuer
    template_name = 'create_view.html'
    form_class = CreateIssuerForm
    success_url = reverse_lazy('badge_home')
    class_name = 'Issuer'


class IssuerUpdateView(ClassNameMixin, UpdateView):
    model = Issuer
    template_name = 'update_view.html'
    success_url = reverse_lazy('badge_home')
    class_name = 'Issuer'
    fields = ['name', 'initials', 'url',
              'doc_path', 'desc', 'image', 'contact']


class BadgeListView(ClassNameMixin, ListView):
    model = Badge
    template_name = 'list_view.html'
    class_name = 'Badge'


class BadgeCreateView(ClassNameMixin, CreateView):
    model = Badge
    template_name = 'create_badge_view.html'
    form_class = CreateBadgeForm
    class_name = 'Badge'
    badge_issuer = None

    def get_success_url(self):
        return reverse_lazy('create_badge_by_issuer', args=[self.badge_issuer.id])

    def get_initial(self):
        self.badge_issuer = get_object_or_404(Issuer, pk=self.kwargs['issuer'])
        initial = self.initial.copy()
        initial['issuer'] = self.badge_issuer
        initial['creator'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(BadgeCreateView, self).get_context_data(**kwargs)
        context['current_objects'] = Badge.objects.filter(
            issuer=self.badge_issuer)
        context['parent_object'] = self.badge_issuer
        return context


class BadgeUpdateView(ClassNameMixin, UpdateView):
    model = Badge
    template_name = 'update_view.html'
    class_name = 'Badge'
    fields = ['name', 'image', 'description', 'criteria', 'issuer']
    
    def get_success_url(self):
        return reverse_lazy('create_badge_by_issuer', args=[self.get_object().issuer.id])

class AwardListView(ClassNameMixin, ListView):
    model = Award
    template_name = 'list_view.html'
    class_name = 'Award'

    def get_queryset(self):
        try:
            badge_id = self.kwargs['pk']
            self.queryset = Award.objects.filter(badge__id=badge_id)
        except:
            pass

        return super(AwardListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(AwardListView, self).get_context_data(**kwargs)
        try:
            context['obj_filter'] = Badge.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return context


class AwardCreateView(ClassNameMixin, CreateView):
    model = Award
    template_name = 'create_award_view.html'
    form_class = CreateAwardForm
    class_name = 'Award'
    badge_to_award = None

    def get_success_url(self):
        return reverse_lazy('create_award_by_badge', args=[self.badge_to_award.id])

    def get_initial(self):
        self.badge_to_award = get_object_or_404(Badge, pk=self.kwargs['badge'])
        initial = self.initial.copy()
        initial['badge'] = self.badge_to_award
        initial['creator'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(AwardCreateView, self).get_context_data(**kwargs)
        context['current_objects'] = Award.objects.filter(
            badge=self.badge_to_award)
        context['parent_object'] = self.badge_to_award
        return context


class AwardUpdateView(ClassNameMixin, UpdateView):
    model = Award
    template_name = 'update_view.html'
    class_name = 'Award'
    fields = ['email', 'firstname', 'lastname',
              'badge', 'creator', 'evidence', 'expires']
    
    def get_success_url(self):
        return reverse_lazy('create_award_by_badge', args=[self.get_object().badge.id])

class RevokeAwardView(ClassNameMixin, CreateView):
    model = Revocation
    template_name = 'revoke_award_view.html'
    award_to_revoke = None
    form_class = RevokeAwardForm
    class_name = 'Revocation'


    def get_success_url(self):
        return reverse_lazy('revoke_award', args=[self.award_to_revoke.id])

    def get_initial(self):
        self.award_to_revoke = get_object_or_404(Award, pk=self.kwargs['award_to_revoke'])
        initial = self.initial.copy()
        initial['issuer'] = self.award_to_revoke.badge.issuer
        initial['award'] = self.award_to_revoke

        return initial

    def get_context_data(self, **kwargs):
        context = super(RevokeAwardView, self).get_context_data(**kwargs)
        context['form'].fields['award'].label = '%s -- %s' % (self.award_to_revoke.badge, self.award_to_revoke)
        context['current_objects'] = Revocation.objects.all().order_by('issuer')
        context['parent_object'] = 'Revocation'
        return context 








