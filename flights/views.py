from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Flight
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FlightForm
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.urls import reverse_lazy
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.http import Http404


class FlightModelMixin(object):
    model = Flight

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(active=True)

    template_name = 'flights/list.html'


class FlightOwnerMixin(object):
    model = Flight
    template_name = 'flights/mine.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(customer=self.request.user)


class FlightsListView(LoginRequiredMixin, FlightModelMixin, ListView):
    paginate_by = 4


class FlightDetailView(FlightModelMixin, CsrfExemptMixin, JsonRequestResponseMixin, DetailView):
    template_name = 'flights/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.customer == self.request.user:
            context['is_owner'] = 1
            context['list_customers'] = self.object.bookings.all()
        else:
            context['is_in_list'] = 1 if self.request.user in self.object.bookings.all() else 0
        return context

    def post(self, request, *args, **kwargs):
        self.get_object().bookings.add(request.user)
        return redirect(reverse_lazy('flights:detail',
                                     kwargs={'pk': self.get_object().id,
                                             'slug': self.get_object().slug}))


class MineOrders(LoginRequiredMixin, FlightOwnerMixin, ListView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['form'] = FlightForm
        return context


class CreateFlight(CsrfExemptMixin, JsonRequestResponseMixin, CreateView):
    form_class = FlightForm
    success_url = reverse_lazy('flights:mine')

    def get(self, request, *args, **kwargs):
        try:
            super().get(args, kwargs)
        except:
            return redirect(reverse_lazy('flights:mine'))

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.customer = self.request.user
            form.instance.slug = slugify(unidecode(form.instance.flightnumb))

            return super().form_valid(form)
        return redirect(reverse_lazy('users:login'))


class EditFlight(LoginRequiredMixin, UpdateView):
    model = Flight
    success_url = reverse_lazy('flights:mine')
    template_name = 'flights/edit.html'
    form_class = FlightForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.slug = slugify(unidecode(form.instance.flightnumb))

            return super().form_valid(form)
        return redirect(reverse_lazy('users:login'))


class DeleteFlight(LoginRequiredMixin, DeleteView):
    model = Flight
    success_url = reverse_lazy('flights:mine')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.customer == self.request.user:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



