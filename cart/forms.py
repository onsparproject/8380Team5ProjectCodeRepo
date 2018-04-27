from django import forms
from uuid import uuid4

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

class CouponForm(forms.Form):
    CHOICES=[('30% OFF Applied!','Onspar Special Coupon:30% OFF'), ('Free Shipping Applied!','Onspar Free Shipping')]
    coupons = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
