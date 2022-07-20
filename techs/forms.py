from django.forms import ModelForm
from marshmallow import EXCLUDE
from .models import (
    TestResult,
    Phone,
    PhoneComment
)

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = "__all__"

class Locked_TestResultForm(ModelForm):
    class Meta:
        model = TestResult
        fields = "__all__"
        exclude = (
            'label_cost',
            'lcd',
            'digitizer',
            'rear_camera',
            'front_camera',
            'baseband',
            'face_id',
            'wifi_bluetooth',
            'sound',
            'charging_port',
            'housing',
            'unlock_price_table',
            'total_repair_cost',
        )

class NewTestResultForm(ModelForm):
    class Meta:
        model = TestResult
        fields = "__all__"
                
class Unlock_TestResultForm(ModelForm):
    class Meta:
        model = TestResult
        # fields = "__all__"
        exclude = (
            'locked_labor_cost', 
            'locked_screen', 
            'locked_housing',
            'locked_back_camera',
            'locked_charging_port',
            'locked_price_table',
            'has_profit',
            )

class PhoneCommentForm(ModelForm):
    class Meta:
        model = PhoneComment
        fields = "__all__"