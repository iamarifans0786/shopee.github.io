from django import forms
from order.models import Order


class PlaceOrderForm(forms.ModelForm):
    """For Display and Update Billing Phone No. & Address To Checkout Page"""

    class Meta:
        model = Order
        fields = ["mobile", "address"]

    def __init__(self, *args, **kwargs):
        super(PlaceOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
