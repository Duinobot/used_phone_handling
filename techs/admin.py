from django.contrib import admin
import requests
from .models import (
    TestResult,
    Phone,
    PhoneComment,
)
from .forms import (
    Unlock_TestResultForm,
    PhoneForm,
    Locked_TestResultForm,
    NewTestResultForm
)

from django import forms
from django.urls import path, re_path, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .handle_csv_upload import handle_csv_upload
from .validators import import_csvfile_validator
from django.core.validators import FileExtensionValidator
# CSV Upload form for phones admin page
class CSVUploadForm(forms.Form):
    csvfile = forms.FileField(
        required=True,
        label="Select CSV file",
        validators=[
        FileExtensionValidator(['csv','xlsx']), 
        import_csvfile_validator,]
        )

class CustomPhoneCommentAdmin(admin.TabularInline):
    model = PhoneComment
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra

@admin.action(description='0. Check Selected if Locked')
def check_if_locked(modeladmin, request, queryset):
    # API info
    URL = 'http://gsxunlocking.com:12962/api.php'
    user = "imobile"
    key = "W8I8-H5L4-H1F7-R2P6-Q5V0"
    service_id = 2019
    
    for phone in queryset:
        # check lock status and update website
        imei = phone.imei
        print(imei)
        PARAMS = {'user': user, 'key': key, 'id': service_id, 'imei': imei}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        if data['flag'] == 'ok':
            if 'Off' in data['result']:
                print('Unlock')
                phone.is_locked='UN'
                phone.save()
            else:
                print('locked')
                phone.is_locked='LO'
                phone.save()
        elif data['flag'] == 'fail':
            print('failed')
            phone.is_locked='FA'
            phone.save()

@admin.register(Phone)
class CustomPhoneAdmin(admin.ModelAdmin):
    change_list_template = "admin/techs/phone/change_list.html"
    form = PhoneForm
    autocomplete_fields = ['phonespec']
    exclude = ["name"]
    readonly_fields = ['fixed_by',]
    search_fields = ['name', 'imei']
    actions = [check_if_locked]
    inlines = [
        CustomPhoneCommentAdmin,
    ]
    list_display = ('__str__','brand', 'is_locked', 'certificate')
    list_filter = ('phonespec__model__brand', 'is_locked', 'is_ready_for_sales')

    def get_changeform_initial_data(self, request):
        get_data = super(CustomPhoneAdmin, self).get_changeform_initial_data(request)
        get_data['add_by'] = request.user.pk
        print(get_data['add_by'])
        return get_data

    def changelist_view(self, request, *args, **kwargs):
        view = super().changelist_view(request, *args, **kwargs)
        if request.method == 'GET':
            view.context_data['submit_csv_form'] = CSVUploadForm
        return view

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('upload-csv/', self.upload_csv, name='upload_csv'),]
        return my_urls + urls
    
    def upload_csv(self, request, *args, **kwargs):
        # if request.method == 'GET':
        #     return render(request, reverse('admin:techs_phone_changelist'), {"form": CSVUploadForm()})
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if not form.is_valid():
                print(form.errors)
                return HttpResponse(form.errors.values())
            handle_csv_upload(request.FILES['csvfile'])
            return HttpResponseRedirect('/techs/phone/')

@admin.register(TestResult)
class CustomTestResultAdmin(admin.ModelAdmin):
    autocomplete_fields = ['phone']
    search_fields = ['phone__name', 'phone__imei']
    readonly_fields= ('has_profit',)
    list_display = ('__str__', 'is_tested', 'has_profit')
    list_filter = ('is_tested', 'has_profit')

    def get_changeform_initial_data(self, request):
        get_data = super(CustomTestResultAdmin, self).get_changeform_initial_data(request)
        get_data['technician'] = request.user.pk
        return get_data

    def get_form(self, request, obj=None, **kwargs):
        if obj == None:
            kwargs['form'] = NewTestResultForm
            return super().get_form(request, obj, **kwargs)
        elif obj.phone.is_locked == "LO":
            return Locked_TestResultForm
        elif obj.phone.is_locked == "UN":
            return Unlock_TestResultForm
    

