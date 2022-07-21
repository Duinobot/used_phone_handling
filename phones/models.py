import uuid
from django.db import models
from django.urls import reverse


# Refer to model diagram https://drive.google.com/file/d/1LH1cB47npNIQdXnyk0o0fInNFF3cTHk8/view?usp=sharing

class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    brand = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('brand_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "2. Brand"


class Model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    model = models.CharField(max_length=50, unique=True)
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
        verbose_name = "0. Model and Part Price"


class Color(models.Model):
    color = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.color

    def get_absolute_url(self):
        return reverse('model_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "3. Color"


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
        verbose_name = "[Locked] Parts Value"


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
        verbose_name = "[Unlocked] Parts Cost"


class PhoneSpec(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.CharField(max_length=50, null=True, blank=True)
    fullname = models.CharField(max_length=30, null=True, blank=True)
    model = models.ForeignKey(
        Model,
        related_name='phonespec',
        on_delete=models.PROTECT
    )

    MemorySize = [
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
    ]
    storage = models.CharField(max_length=5, choices=MemorySize, default='64GB')
    color = models.ForeignKey(Color, related_name='phonespec', on_delete=models.PROTECT)
    listing_id = models.IntegerField(null=True, blank=True)
    sku = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):            
        if not self.fullname:
            self.fullname = str(self.model) + " " + self.storage + " [" + str(self.color.color) + "]"
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fullname)

    def get_absolute_url(self):
        return reverse('phonespec_detail', arg=[str(self.id)])


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'storage', 'color'], name='unique_phonespec_detail')
        ]

        verbose_name = "1. Phone Specs"


class Location(models.Model):
    location = models.CharField(max_length=10)

    def __str__(self):
        return self.location

    def get_absolute_url(self):
        return reverse('location_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "5. Location"

class Grade(models.Model):
    grade = models.CharField(max_length=1)

    def __str__(self):
        return self.grade + " Grade"

    def get_absolute_url(self):
        return reverse('grade_detail', arg=[str(self.id)])

    class Meta:
        verbose_name = "4. Grades"



