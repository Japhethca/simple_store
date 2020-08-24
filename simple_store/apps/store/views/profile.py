from django.shortcuts import (
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import DeleteView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import QueryDict

from simple_store.apps.core.models import BillingAddress
from ..forms import (
    AddressForm,
    ProfileForm,
)


User = get_user_model()


class CustomerProfile(LoginRequiredMixin, ListView):
    template_name = "store/pages/customer-profile.html"
    login_url = "/accounts/login"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_form"] = ProfileForm(initial=model_to_dict(self.request.user))
        return context


class CustomerReviews(LoginRequiredMixin, ListView):
    template_name = "store/pages/customer-reviews.html"
    login_url = "/accounts/login"
    queryset = []


class CustomerAddress(LoginRequiredMixin, ListView):
    template_name = "store/pages/customer-address.html"
    login_url = "/accounts/login"
    model = BillingAddress
    context_object_name = "addresses"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_addresses = queryset.filter(customer=self.request.user)
        return user_addresses

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["new_address_form"] = AddressForm()
        return context


class CustomerAddressNew(LoginRequiredMixin, FormView):
    template_name = "store/pages/customer-address-new.html"
    login_url = "/accounts/login"
    form_class = AddressForm
    model = BillingAddress

    def get_success_url(self):
        return f"{reverse('customer-address')}?{self.request.META['QUERY_STRING']}"

    def get_initial(self):
        if (address_pk := self.kwargs.get("pk", None)) is not None:
            address_object = get_object_or_404(self.model, pk=address_pk)
            return model_to_dict(address_object)

        initial = {
            "first_name": self.request.user.first_name or None,
            "last_name": self.request.user.last_name or None,
        }
        return initial

    def form_valid(self, form):
        address_pk = self.kwargs.get("pk", None)
        form_object = self.model(**form.cleaned_data)
        form_object.customer = self.request.user
        form_object.pk = address_pk
        form_object.save()
        return super().form_valid(form)


class CustomerAddressDelete(LoginRequiredMixin, DeleteView):
    model = BillingAddress
    login_url = "/accounts/login"

    def get_success_url(self):
        return f"{reverse('customer-address')}?{self.request.META['QUERY_STRING']}"


class CustomerAddressSetDefault(LoginRequiredMixin, View):
    model = BillingAddress
    login_url = "/accounts/login"
    http_method_names = ["post"]

    def post(self, request, **kwargs):
        address_pk = kwargs.get("pk")
        address_model = self.model.objects.get(pk=address_pk)
        self.model.set_as_default(address_model)
        return self.handle_redirect(request)

    def handle_redirect(self, request):
        supported_reqirects = [reverse("checkout")]
        qd = QueryDict(self.request.META["QUERY_STRING"])
        next_url = qd.get("next")
        if next_url in supported_reqirects:
            return redirect(next_url)
        return redirect(reverse("customer-address"))


class CustomerFavorites(LoginRequiredMixin, ListView):
    template_name = "store/pages/customer-favorites.html"
    login_url = "/accounts/login"
    queryset = []
