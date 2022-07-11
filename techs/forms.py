from dataclasses import field, fields
from django.forms import ModelForm
from .models import (
    TestResult,
    Phone,
    PhoneComment
)

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = "__all__"

class TestResultForm(ModelForm):
    class Meta:
        model = TestResult
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Render ModelForm base on locked status
        self.fields['is_tested'].disabled =True
        if self.instance.is_tested == True:
            if self.instance.phone.is_locked == "LO":
                self.fields['label_cost']
                self.fields['lcd'].disabled =True
                self.fields['digitizer'].disabled =True
                self.fields['rear_camera'].disabled =True
                self.fields['front_camera'].disabled =True
                self.fields['baseband'].disabled =True
                self.fields['face_id'].disabled =True
                self.fields['wifi_bluetooth'].disabled =True
                self.fields['sound'].disabled =True
                self.fields['charging_port'].disabled =True
                self.fields['housing'].disabled =True
                self.fields['unlock_price_table'].disabled =True
                self.fields['total_repair_cost'].disabled =True

            elif self.instance.phone.is_locked == "UN":
                self.fields['locked_labor_cost'].disabled =True
                self.fields['locked_screen'].disabled = True
                self.fields['locked_housing'].disabled =True
                self.fields['locked_back_camera'].disabled =True
                self.fields['locked_charging_port'].disabled =True
                self.fields['locked_price_table'].disabled =True
                



class PhoneCommentForm(ModelForm):
    class Meta:
        model = PhoneComment
        fields = "__all__"