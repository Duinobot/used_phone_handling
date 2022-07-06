from tabnanny import verbose
from django.conf import settings
import uuid
from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Refer to model diagram https://drive.google.com/file/d/1LH1cB47npNIQdXnyk0o0fInNFF3cTHk8/view?usp=sharing

class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    brand = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('brand_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "1. Brand"


class Model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    model = models.CharField(max_length=20, unique=True)
    brand = models.ForeignKey(
        Brand,
        related_name="models",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('model_detail', args=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'brand'], name="unique_model_brand")
        ]
        verbose_name = "2. Phone Model"


class Color(models.Model):
    color = models.CharField(max_length=10)
    model = models.ForeignKey(
        Model,
        related_name='colors',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.color + " (" + str(self.model) + ")"

    def get_absolute_url(self):
        return reverse('model_detail', args=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'color'], name="unique_color_for_model")
        ]
        verbose_name = "3. Phone Color"


class Storage(models.Model):
    MemorySize = [
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
    ]
    model = models.ForeignKey(
        Model,
        related_name='storages',
        on_delete=models.CASCADE
    )
    storage = models.CharField(max_length=5, choices=MemorySize)

    def __str__(self):
        return self.storage + " (" + str(self.model) + ")"

    def get_absolute_url(self):
        return reverse('storage_detail', arg=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'storage'], name="unique_storage_for_model")
        ]
        verbose_name = "4. Phone Storage"


class PurchasePrice(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    storage = models.ForeignKey(
        Storage,
        related_name='purchase_prices',
        on_delete=models.RESTRICT
    )
    model = models.ForeignKey(
        Model,
        related_name='purchase_prices',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.model) + " " + str(self.storage.storage) + " (purchase price: $" + str(self.purchase_price) + ")"
    
    def get_absolute_url(self):
        return reverse('purchase_price_detail', arg=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'storage'], name='unique_price_give_model_and_storage')
        ]
        verbose_name = "5. Purchase Price"


class LockedPartsWorth(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    model = models.OneToOneField(Model, on_delete=models.CASCADE, related_name="parts_worth")
    screen = models.DecimalField(max_digits=6, decimal_places=2)
    housing = models.DecimalField(max_digits=6, decimal_places=2)
    back_camera = models.DecimalField(max_digits=6, decimal_places=2)
    charging_port = models.DecimalField(max_digits=6, decimal_places=2)

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.model) + " Parts Worth"

    def get_absolute_url(self):
        return reverse('lockedpartsworth_detail', arg=[str(self.id)])
    
    class Meta:
        verbose_name = "6. [Locked] Parts Value"


class UnlockedPartsCost(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    model = models.OneToOneField(Model, on_delete=models.CASCADE, related_name="parts_cost")
    lcd = models.DecimalField(max_digits=6, decimal_places=2)
    digitizer = models.DecimalField(max_digits=6, decimal_places=2)
    rear_camera = models.DecimalField(max_digits=6, decimal_places=2)
    front_camera = models.DecimalField(max_digits=6, decimal_places=2)
    baseband = models.DecimalField(max_digits=6, decimal_places=2)
    face_id = models.DecimalField(max_digits=6, decimal_places=2)
    wifi_bluetooth = models.DecimalField(max_digits=6, decimal_places=2)
    sound = models.DecimalField(max_digits=6, decimal_places=2)
    charging_port = models.DecimalField(max_digits=6, decimal_places=2)
    housing = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.model) + " Repair Parts Cost"

    def get_absolute_url(self):
        return reverse('unlockedpartscost_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "7. [Unlocked] Parts Cost"


class PhoneSpec(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    fullname = models.CharField(max_length=30, null=True, blank=True)
    model = models.ForeignKey(
        Model,
        related_name='phonespec',
        on_delete=models.PROTECT
    )
    purchase_price = models.ForeignKey(PurchasePrice, related_name='phonespec', on_delete=models.SET_NULL, null=True, blank=True)
    storage = models.ForeignKey(Storage, related_name='phonespec', on_delete=models.PROTECT)
    color = models.ForeignKey(Color, related_name='phonespec', on_delete=models.PROTECT)
    listing_id = models.IntegerField(null=True, blank=True)
    sku = models.IntegerField(null=True, blank=True)

    def lookup_purchase_price(self):
        return PurchasePrice.objects.get(model=self.model, storage=self.storage)

    def clean(self):
        if not self.purchase_price:
            try:
                self.purchase_price = self.lookup_purchase_price()
            except ObjectDoesNotExist:
                raise ValidationError("Purchase price for model doesn't exsit, please add it first.")

    def save(self, *args, **kwargs):            
        if not self.fullname:
            self.fullname = str(self.model) + " " + str(self.storage.storage) + " [" + str(self.color.color) + "]"
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fullname)

    def get_absolute_url(self):
        return reverse('phonespec_detail', arg=[str(self.id)])


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'storage', 'color', 'purchase_price'], name='unique_phonespec_detail')
        ]

        verbose_name = "0. Phone Specification"


class Location(models.Model):
    location = models.CharField(max_length=10)

    def __str__(self):
        return self.location

    def get_absolute_url(self):
        return reverse('location_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "9. Phone Location"

class Grade(models.Model):
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.grade + " Grade"

    def get_absolute_url(self):
        return reverse('grade_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "8. Phone Grade"



