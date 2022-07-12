from django.contrib import admin

from .models import (
    TestResult,
    Phone,
    PhoneComment,
)
from .forms import (
    Unlock_TestResultForm,
    PhoneForm,
    Locked_TestResultForm
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



@admin.register(TestResult)
class CustomTestResultAdmin(admin.ModelAdmin):
    # form = TestResultForm
    autocomplete_fields = ['phone']
    search_fields = ['phone__name', 'phone__imei']
    readonly_fields= ('has_profit',)

    def get_changeform_initial_data(self, request):
        get_data = super(CustomTestResultAdmin, self).get_changeform_initial_data(request)
        get_data['technician'] = request.user.pk
        print(get_data['technician'])
        print(self.obj)
        return get_data

    def get_form(self, request, obj=None, **kwargs):
        if obj.phone.is_locked == "LO":
            return Locked_TestResultForm
        elif obj.phone.is_locked == "UN":
            return Unlock_TestResultForm
    

