from decimal import Decimal
import pandas as pd
from .models import Phone
from phones.models import Brand, Color, Model, PhoneSpec
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse

def handle_csv_upload(phones_file):
    
    print("entering csv handle")
    extension = phones_file.name.split(".")[-1].lower()
    if extension == 'csv':
        
        # csv_file = TextIOWrapper(phones_file, encoding="utf-8", newline="")
        df = pd.read_csv(phones_file.open())
        # print(TextIOWrapper(phones_file, encoding="utf-8", newline="").closed)
        # print(df)
        
        # df = pd.read_csv(csvfile)
    elif extension == "xlsx":
        df = pd.read_excel(phones_file)

    df = df.rename(columns=lambda x: x.strip())
    df['Color'] = df['Color'].apply(lambda x: x.strip().title())
    df['Price Inc'] = df['Price Inc'].apply(lambda price: price if type(price)==float else float(price.strip('$ ').replace(',','')))
    df['Price Ex'] = df['Price Inc'].apply(lambda x: float("{:.2f}".format(x/1.1)))
    df['IMEI'] = df['IMEI'].apply(str)
    # Check and add new Model.
    # 1 get unique model value
    uploaded_models = df["Model"].unique()


    # Add phonespec
    # 1 check if model + color + storage in phonespec model
    # 2 if not add phonespec
    for model in uploaded_models:
        model_df = df[df.Model==model]
        dj_brand, created = Brand.objects.get_or_create(brand=model_df.iloc[0]['Manufacturer'])
        dj_model, created = Model.objects.get_or_create(model=model, brand=dj_brand)
        for index, row in model_df.iterrows():
            if pd.isnull(row['Color']):
                raise ValidationError('Color is empty for ' + row['Description'])
            if '16GB' in row['Description']:
                storage = '16GB'
            elif '32GB' in row['Description']:
                storage = '32GB'
            elif '64GB' in row['Description']:
                storage = '64GB'
            elif '128GB' in row['Description']:
                storage = '128GB'
            elif '256GB' in row['Description']:
                storage = '256GB'
            elif '512GB' in row['Description']:
                storage = '512GB'
            elif '1TB' in row['Description']:
                storage = '1TB'
            else:
                raise ValidationError('Cannot find storage for ' + row['Description'])
            dj_color, created = Color.objects.get_or_create(color=row['Color'].title())
            
            dj_phonespec, created = PhoneSpec.objects.get_or_create(
                model=dj_model,
                storage=storage,
                color=dj_color,
                )

            # Add phones
            phone, created = Phone.objects.update_or_create(
                phonespec=dj_phonespec,
                imei=row['IMEI'],
                )
            print(phone.imei)
            print(row['Price Ex'])
            print(row['C SKU'])
            Phone.objects.filter(imei=phone.imei).update(
                purchase_price=row['Price Ex'],vendor_sku=row['C SKU'],)