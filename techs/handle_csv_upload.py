import pandas as pd

from .models import Phone
from phones.models import Brand, Color, Model, PhoneSpec

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
    print(str(df))

    # Check and new brand exists.
    # 1 get unique Manufacturer value
    uploaded_brands = df["Manufacturer"].unique()
    # 2 check if value in Brand model
    # 3 if not, add brand
    for brand in uploaded_brands:
        Brand.objects.get_or_create(brand=brand)
    Brand.save()
        




    # Check and add new color.
    # 1 get unique Color value
    uploaded_colors = df["Color"].unique()
    # 2 check if value in Color model
    # 3 if not, add color
    for color in uploaded_colors:
        Color.objects.get_or_create(color=color)
    Color.save()

    # Check and add new Model.
    # 1 get unique model value
    uploaded_model = df["Color"].unique()
    # 2 check if value in Model model
    # 3 if not add model, passing brand
    for model in uploaded_model:
        Model.objects.get_or_create(model=model, brand=df[df.Model==model].Manufacturer.values[0])
    Model.save()

    # Add phonespec
    # 1 check if model + color + storage in phonespec model
    # 2 if not add phonespec

    # Add phones.