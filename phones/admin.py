from django.contrib import admin
from .models import (
    Brand,
    Model,
    Color,
    Storage,
    LockedPartsWorth,
    UnlockedPartsCost,
    PhoneSpec,
    Location,
    Grade,
)
from .forms import (
    BrandForm,
    ModelsForm,
    ColorForm,
    StorageForm,
    LockedPartsWorthPriceForm,
    UnlockedPartsCostForm,
    PhoneSpecForm,
    LocationForm,
    GradeForm,
)

# Register your models here.

@admin.register(Brand)
class CustomBrandAdmin(admin.ModelAdmin):
    form = BrandForm

@admin.register(Model)
class CustomModelsAdmin(admin.ModelAdmin):
    form = ModelsForm


@admin.register(Color)
class CustomColorAdmin(admin.ModelAdmin):
    form = ColorForm


@admin.register(Storage)
class CustomStorageAdmin(admin.ModelAdmin):
    form = StorageForm

@admin.register(LockedPartsWorth)
class CustomLockedPartsWorthAdmin(admin.ModelAdmin):
    form = LockedPartsWorthPriceForm


@admin.register(UnlockedPartsCost)
class CustomUnlockedPartsCostAdmin(admin.ModelAdmin):
    form = UnlockedPartsCostForm


@admin.register(PhoneSpec)
class CustomPhoneSpecAdmin(admin.ModelAdmin):
    form = PhoneSpecForm
    readonly_fields = ["fullname",]
    search_fields = ['model__model', 'storage__storage', 'color__color', 'sku', 'listing_id']
    # search_fields = ['model__model', 'listing_id' , 'sku', 'listing_id']


@admin.register(Location)
class CustomLocationAdmin(admin.ModelAdmin):
    form = LocationForm


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    form = GradeForm









