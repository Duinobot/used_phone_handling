from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import TestResultUnlocked, TestResultLocked

@receiver(post_save,sender=TestResultUnlocked)
def update_final_worth_unlocked(sender, instance, update_fields, **kwargs):
    instance.phone.final_cost = instance.final_worth
    instance.phone.save()

@receiver(post_save,sender=TestResultLocked)
def update_final_worth_unlocked(sender, instance, update_fields, **kwargs):
    print("updating final cost Locked", update_fields)
    instance.phone.final_cost = instance.final_worth
    instance.phone.save()