import io
from io import TextIOWrapper
import pandas as pd
import csv

def handle_csv_upload(phones_file):
    
    print("entering csv handle")
    extension = phones_file.name.split(".")[-1].lower()
    if extension == 'csv':
        
        # csv_file = TextIOWrapper(phones_file, encoding="utf-8", newline="")
        df = pd.read_csv(phones_file.open())
        # print(TextIOWrapper(phones_file, encoding="utf-8", newline="").closed)
        print(df)
        
        # df = pd.read_csv(csvfile)
    elif extension == "xlsx":
        df = pd.read_excel(phones_file)
    
    print(str(df.iloc[0]))


    # Check and new brand exists.

    # Check and add new color.

    # Check and add new Model.

    # Add phones.