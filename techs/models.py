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
        if self.is_locked == "LO":
            return str(self.name) + " (" + self.imei + ")" + " (Locked)"
        elif self.is_locked == "UN":
            return str(self.name) + " (" + self.imei + ")" + " (Unlock)"
        else:
            return str(self.name) + " (" + self.imei + ")" + " (Pending)"


    def get_absolute_url(self):
        return reverse('phone_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "1. All Phones"

class TestResult(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone = models.OneToOneField(Phone, on_delete=models.CASCADE, related_name="test_form")
    is_tested = models.BooleanField(verbose_name="Is phone tested?")

    # If Unlock:
    label_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
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

    unlock_price_table = models.ForeignKey(UnlockedPartsCost, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Part Price (Autofilled)")
    total_repair_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    has_profit = models.BooleanField(verbose_name="Ok to repair",default=False)

    # If Locked:
    locked_labor_cost = models.DecimalField(max_digits=6, decimal_places=2, default=15)
    locked_screen = models.BooleanField(verbose_name="Screen OK")
    locked_housing = models.BooleanField(verbose_name="Housing OK")
    locked_back_camera = models.BooleanField(verbose_name="Back Camera OK")
    locked_charging_port = models.BooleanField(verbose_name="Charging Port OK")

    locked_price_table = models.ForeignKey(LockedPartsWorth, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Part Worth (Autofilled)")

    # Final Worth
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

    def cal_profit(self):
        try:
            purchase_price = self.phone.purchase_price
        except ObjectDoesNotExist:
            raise ValidationError("Purchase price not available. Please add it first")
        
        return purchase_price - self.total_repair_cost

    def cal_unlock_total_repair_cost(self):
        self.total_repair_cost = (
                self.unlock_price_table.lcd * self.lcd +
                self.unlock_price_table.digitizer * self.digitizer +
                self.unlock_price_table.rear_camera * self.rear_camera +
                self.unlock_price_table.front_camera * self.front_camera +
                self.unlock_price_table.baseband * self.baseband +
                self.unlock_price_table.face_id * self.face_id +
                self.unlock_price_table.wifi_bluetooth * self.wifi_bluetooth +
                self.unlock_price_table.sound * self.sound +
                self.unlock_price_table.charging_port * self.charging_port +
                self.unlock_price_table.housing * self.housing +
                self.label_cost
            )

    def cal_locked_final_worth(self):
        self.final_worth = (
            self.locked_screen * self.locked_price_table.screen +
            self.locked_housing * self.locked_price_table.housing +
            self.locked_back_camera * self.locked_price_table.back_camera +
            self.locked_charging_port * self.locked_price_table.charging_port -
            self.locked_labor_cost
        )



    def clean(self):
        if self.phone.is_locked == "PE":
            raise ValidationError("Is Phone Locked or not？ Check and change lock status first")
        elif self.phone.is_locked == "UN":
            try:
                self.unlock_price_table = self.phone.phonespec.model.parts_cost
            except ObjectDoesNotExist:
                raise ValidationError("Associated price not available. Please add unlocked part cost first")
        elif self.phone.is_locked == "LO":
            try:
                self.locked_price_table = self.phone.phonespec.model.parts_worth
            except ObjectDoesNotExist:
                raise ValidationError("Associated price not available. Please locked part price first")

        if self.has_changed:
            if self.phone.is_locked == "LO":
                self.cal_locked_final_worth()

            if self.phone.is_locked == "UN":
                self.cal_unlock_total_repair_cost()
                profit = self.cal_profit()
                if profit > 0:
                    self.final_worth = profit
                    self.has_profit = True
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
                    self.has_profit = False

    def save(self, *args, **kwargs):
        if self.has_changed:
            self.is_tested = True
        super().save(*args, **kwargs)

    def __str__(self):
        if self.phone.is_locked == "UN":
            return "[Unlocked] Test Result for: " + str(self.phone) + " IMEI:" + str(self.phone.imei)
        if self.phone.is_locked == "LO":
            return "[Locked] Test Result for: " + str(self.phone) + " IMEI:" + str(self.phone.imei)


    def get_absolute_url(self):
        return reverse('test_result', args=[str(self.id)])

    class Meta:
        verbose_name = "2. Phone Test Result"


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
