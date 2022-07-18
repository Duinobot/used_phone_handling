from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from phones.models import Brand, Model, Color, LockedPartsWorth, UnlockedPartsCost, PhoneSpec, Location, Grade

class Command(BaseCommand):
    help = "a command to import data to phone specs"
    
    def handle(slef, *args, **options):
        
        excel_file = "C:\Users\User\Desktop\phone upload\Lot 4 IMEI detail 240622 iMobile.xlsx"
        df = pd.read_excel(excel_file)
        