from django.contrib import admin

from .models import (
    TestResultLocked,
    TestResultUnlocked,
    Phone,
    PhoneComment,
)
from .forms import (
    TestResultLockedForm,
    TestResultUnlockedForm,
    PhoneForm,
    PhoneCommentForm
)
# Register your models here.

class CustomPhoneCommentAdmin(admin.TabularInline):
    model = PhoneComment
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra

@admin.register(Phone)
class CustomPhoneAdmin(admin.ModelAdmin):
    form = PhoneForm
    autocomplete_fields = ['phonespec']
    exclude = ["name"]
    readonly_fields = ['fixed_by',]
    search_fields = ['name', 'imei']
    inlines = [
        CustomPhoneCommentAdmin,
    ]
    def get_changeform_initial_data(self, request):
        get_data = super(CustomPhoneAdmin, self).get_changeform_initial_data(request)
        get_data['add_by'] = request.user.pk
        print(get_data['add_by'])
        return get_data

@admin.register(TestResultLocked)
class CustomTestResultLockedAdmin(admin.ModelAdmin):
    form = TestResultLockedForm
    autocomplete_fields = ['phone']
    search_fields = ['phone_fullname', 'phone_imei']


@admin.register(TestResultUnlocked)
class CustomTestResultUnlockedAdmin(admin.ModelAdmin):
    form = TestResultUnlockedForm
    autocomplete_fields = ['phone']
    search_fields = ['phone_fullname', 'phone_imei']
    readonly_fields = ['profitless']

