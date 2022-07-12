from tkinter.tix import Tree
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import TestResult

@receiver(post_save,sender=TestResult)
def update_final_worth(sender, instance, update_fields, **kwargs):
    print("updating final cost Locked", update_fields)

    # If Locked
    if instance.has_changed:
        instance.phone.final_cost = instance.final_worth
        instance.phone.save()
    
    # # If Unlock and has profit
    # if instance.phone.is_locked == "UN" and instance.profitless == False:
    #     instance.phone.final_cost = instance.final_worth
    #     instance.phone.save()

    # # If Unlock and no profit
    # if instance.phone.is_locked == "UN" and instance.profitless == True:
    #     instance.phone.final_cost = instance.final_worth
    #     instance.phone.save()


    