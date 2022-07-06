from dataclasses import fields
from django.forms import ModelForm
from .models import (
    Brand,
    Grade,
    Model,
    Color,
    Storage,
    PurchasePrice,
    LockedPartsWorth,
    UnlockedPartsCost,
    PhoneSpec,
    Location,
    Grade,
)

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"

class ModelsForm(ModelForm):
    class Meta:
        model = Model
        fields = "__all__"

class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = "__all__"

class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = "__all__"

class PurchasePriceForm(ModelForm):
    class Meta:
        model = PurchasePrice
        fields = "__all__"

class LockedPartsWorthPriceForm(ModelForm):
    class Meta:
        model = LockedPartsWorth
        fields = "__all__"

class UnlockedPartsCostForm(ModelForm):
    class Meta:
        model = UnlockedPartsCost
        fields = "__all__"

class PhoneSpecForm(ModelForm):
    class Meta:
        model = PhoneSpec
        fields = "__all__"

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = "__all__"