from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Brand,
    Model,
    Color,
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

class BuyPartPrice(admin.SimpleListFilter):
    title = _('Locked Phone Part Price')
    parameter_name = 'lockedphonepartprice'
    def lookups(self, request, model_admin):
        return (
            ('has_price', _('Has Price Table')),
            ('no_price', _('No Price Table')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'has_price':
            return queryset.filter(parts_worth__isnull=False)
        if self.value() == 'no_price':
            return queryset.filter(parts_worth__isnull=True)
        


class RepairPartPrice(admin.SimpleListFilter):
    title = _('iMobile Repair Part Cost')
    parameter_name = 'repairpartcost'
    def lookups(self, request, model_admin):
        return (
            ('has_price', _('Has Price Table')),
            ('no_price', _('No Price Table')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_price':
            return queryset.filter(parts_cost__isnull=False)
        if self.value() == 'no_price':
            return queryset.filter(parts_cost__isnull=True)

@admin.register(Model)
class CustomModelsAdmin(admin.ModelAdmin):
    form = ModelsForm
    list_display = ('brand', '__str__')
    list_filter = ('brand', BuyPartPrice, RepairPartPrice)


@admin.register(Color)
class CustomColorAdmin(admin.ModelAdmin):
    form = ColorForm

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
    search_fields = ['model__model', 'storage', 'color__color', 'sku', 'listing_id']
    # search_fields = ['model__model', 'listing_id' , 'sku', 'listing_id']


@admin.register(Location)
class CustomLocationAdmin(admin.ModelAdmin):
    form = LocationForm


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    form = GradeForm









