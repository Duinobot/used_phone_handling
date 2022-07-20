from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import TestResult, Phone

@receiver(post_save,sender=TestResult)
def update_final_worth(sender, instance, update_fields, **kwargs):
    print("updating final cost Locked", update_fields)

    # If Locked
    if instance.has_changed:
        instance.phone.final_cost = instance.final_worth
        instance.phone.save()
    
@receiver(post_save,sender=Phone)
def update_unlock_status(sender, instance, **kwargs):
    if instance.is_locked != "PE" or instance.is_locked != "FA":
        test_form, created = TestResult.objects.get_or_create(phone=instance)


    # # If Unlock and has profit
    # if instance.phone.is_locked == "UN" and instance.profitless == False:
    #     instance.phone.final_cost = instance.final_worth
    #     instance.phone.save()

    # # If Unlock and no profit
    # if instance.phone.is_locked == "UN" and instance.profitless == True:
    #     instance.phone.final_cost = instance.final_worth
    #     instance.phone.save()


    