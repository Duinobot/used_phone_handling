from django.forms import ModelForm
from .models import (
    TestResultLocked,
    TestResultUnlocked,
    Phone,
    PhoneComment
)

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = "__all__"

class TestResultLockedForm(ModelForm):
    class Meta:
        model = TestResultLocked
        fields = "__all__"

class TestResultUnlockedForm(ModelForm):
    class Meta:
        model = TestResultUnlocked
        fields = "__all__"

class PhoneCommentForm(ModelForm):
    class Meta:
        model = PhoneComment
        fields = "__all__"