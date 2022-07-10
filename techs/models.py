from django.db import models

from django.conf import settings
import uuid
from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import model_to_dict
from phones.models import (
    Grade,
    LockedPartsWorth,
    UnlockedPartsCost,
    PhoneSpec,
    Location,
    Grade,
)

# Refer to model diagram https://drive.google.com/file/d/1LH1cB47npNIQdXnyk0o0fInNFF3cTHk8/view?usp=sharing

class Phone(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phonespec = models.ForeignKey(PhoneSpec, related_name='phones', on_delete=models.PROTECT)
    imei = models.CharField(max_length=60, unique=True)

    LOCK_STATUS = [
        ("PE", "Pending"),
        ("LO", "Locked"),
        ("UN", "Unlock"),
    ]


    is_locked = models.CharField(max_length=2, choices=LOCK_STATUS, default="PE")
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, null=True, blank=True)

    purchase_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
        
    final_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fixed_by = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET_NULL, related_name='repairs', null=True, blank=True)

    vendor_sku = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, related_name='phones', on_delete=models.PROTECT, null=True, blank=True, default=1)
    certificate = models.FileField(upload_to='certificates', blank=True)
    sell_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True) # pending, add later
    date_purchased = models.DateTimeField(null=True, blank=True)

    add_by = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET_NULL, related_name='add_by', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.purchase_price:
            raise ValidationError("Please add purchase price for this model first")

    def save(self, *args, **kwargs):
        if not self.name:
            if not self.grade:
                self.name = str(self.phonespec.fullname)
            else:
                self.name = str(self.phonespec.fullname) + " [" + str(self.grade) + "]"
            
        super().save(*args, **kwargs)

    def __str__(self):
        if self.is_locked:
            return str(self.name) + " (" + self.imei + ")" + " (Locked)"
        return str(self.name) + " (" + self.imei + ")"

    def get_absolute_url(self):
        return reverse('phone_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "1. All Phones"


class TestResultLocked(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone = models.OneToOneField(
        Phone,
        on_delete=models.CASCADE,
        limit_choices_to={'is_locked': True})
    labor_cost = models.DecimalField(max_digits=6, decimal_places=2, default=15)
    screen = models.BooleanField(verbose_name="Screen OK", default=0)
    housing = models.BooleanField(verbose_name="Housing OK")
    back_camera = models.BooleanField(verbose_name="Back Camera OK")
    charging_port = models.BooleanField(verbose_name="Charging Port OK")

    price_table = models.ForeignKey(LockedPartsWorth, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Part Worth (Autofilled)")
    final_worth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Final_worth (Autofilled)")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True) # add later, pending

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial = self._dict

    def clean(self):
        try:
            self.price_table = self.phone.phonespec.model.parts_worth
        except ObjectDoesNotExist:
            raise ValidationError("Associated part worth not available yet. Please add price first")

        if self.has_changed:
            self.final_worth = (
                self.screen * self.price_table.screen +
                self.housing * self.price_table.housing +
                self.back_camera * self.price_table.back_camera +
                self.charging_port * self.price_table.charging_port -
                self.labor_cost
            )

    def __str__(self):
        return "[Locked] Test Result for: " + str(self.phone) + " IMEI:" + str(self.phone.imei)

    def get_absolute_url(self):
        return reverse('test_result_locked', args=[str(self.id)])

    class Meta:
        verbose_name = "2. Locked Phone Test Result"


class TestResultUnlocked(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone = models.OneToOneField(Phone, on_delete=models.CASCADE, limit_choices_to={'is_locked': False})
    label_cost = models.DecimalField(max_digits=6, decimal_places=2)
    lcd = models.BooleanField(verbose_name="LCD Faulty")
    digitizer = models.BooleanField(verbose_name="Digitizer Faulty")
    rear_camera = models.BooleanField(verbose_name="Rear Camera Faulty")
    front_camera = models.BooleanField(verbose_name="Front Camera Faulty")
    baseband = models.BooleanField(verbose_name="Baseband Issue")
    face_id = models.BooleanField(verbose_name="Face ID Issue")
    wifi_bluetooth = models.BooleanField(verbose_name="Wifi/Bluetooth Issue")
    sound = models.BooleanField(verbose_name="Audio Issue")
    charging_port = models.BooleanField(verbose_name="Charging Port Faulty")
    housing = models.BooleanField(verbose_name="Back Cover Broken")

    price_table = models.ForeignKey(UnlockedPartsCost, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Part Price (Autofilled)")
    total_repair_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    final_worth = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Final Worth (Autofilled)')

    profitless = models.BooleanField(verbose_name="No Profit, for Parts Only")

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True) # add later, pending

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial = self._dict

    def cal_profit(self):
        try:
            purchase_price = self.phone.purchase_price
        except ObjectDoesNotExist:
            raise ValidationError("Purchase price not available. Please add it first")
        
        return purchase_price - self.total_repair_cost

    def clean(self):
        try:
            self.price_table = self.phone.phonespec.model.parts_cost
        except ObjectDoesNotExist:
            raise ValidationError("Associated part cost not available yet. Please add price first")

        if self.has_changed:
            self.total_repair_cost = (
                self.price_table.lcd * self.lcd +
                self.price_table.digitizer * self.digitizer +
                self.price_table.rear_camera * self.rear_camera +
                self.price_table.front_camera * self.front_camera +
                self.price_table.baseband * self.baseband +
                self.price_table.face_id * self.face_id +
                self.price_table.wifi_bluetooth * self.wifi_bluetooth +
                self.price_table.sound * self.sound +
                self.price_table.charging_port * self.charging_port +
                self.price_table.housing * self.housing +
                self.label_cost
            )

        profit = self.cal_profit()
        
        if profit > 0:
            self.final_worth = profit
            self.profitless = False
        else:
            try:
                self.worth_table = self.phone.phonespec.model.parts_worth
            except ObjectDoesNotExist:
                raise ValidationError("Associated part cost not available yet. Please add part worth first")

            self.final_worth = (
                self.worth_table.screen * (1-self.lcd) * (1-self.digitizer) + 
                self.worth_table.housing * (1-self.housing) +
                self.worth_table.back_camera * (1-self.rear_camera) +
                self.worth_table.charging_port * (1-self.charging_port) -
                15
            )
            self.profitless = True



    def __str__(self):
        return "[Unlocked] Test Result for: " + str(self.phone) + " IMEI:" + str(self.phone.imei)

    def get_absolute_url(self):
        return reverse('test_result_unlocked', args=[str(self.id)])

    class Meta:
        verbose_name = "3. Unlocked Phone Test Result"


class PhoneComment(models.Model):
    comment = models.TextField()
    phone = models.ForeignKey(Phone, related_name='comments', on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:25]

    def get_absolute_url(self):
        return reverse('comment_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "4. Comments"
