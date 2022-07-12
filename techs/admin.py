from ast import pattern
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

from django import forms
from django.urls import path, re_path
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .handle_csv_upload import handle_csv_upload

# CSV Upload form for phones admin page
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(required=True, label="Please select a file")


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

    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        view.context_data['submit_csv_form'] = CSVUploadForm
        return view

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [re_path(r'^upload-csv/$', self.upload_csv, name='upload_csv'),]
        return my_urls + urls
    
    def upload_csv(self, request):
        if request.method == 'POST':
            handle_csv_upload(request.FILES['csv_file'])
            # if form.is_valid():
            #     print("Got it"+form)
            #     # process form
            return HttpResponseRedirect('/techs/phone/')


    


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
    

