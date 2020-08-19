from django import forms
from django.contrib.auth import get_user_model
from simple_store.apps.core.models import BillingAddress


User = get_user_model()


BANK = "bank"
CREDIT_CARD = "card"

PAYMENT_METHODS = ((BANK, "Bank"), (CREDIT_CARD, "Credit Card"))


class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS, required=True, widget=forms.RadioSelect
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddressChoiceForm(forms.Form):
    address = forms.ChoiceField(widget=forms.RadioSelect, choices=[])

    def __init__(self, *args, **kwargs):
        address_choices = kwargs.pop("address_choices", ())
        super().__init__(*args, **kwargs)
        self.fields["address"].choices = address_choices


class ProfileForm(forms.ModelForm):
    class Meta:
        fields = ["first_name", "last_name", "email"]
        model = User
