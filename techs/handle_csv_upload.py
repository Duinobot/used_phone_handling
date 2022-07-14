from io import BytesIO
import io
from io import TextIOWrapper
import pandas as pd

def handle_csv_upload(phones_file):
    
    print("entering csv handle")
    extension = phones_file.name.split(".")[-1].lower()
    if extension == 'csv':
        pass
        # df = pd.read_csv(csvfile)
    elif extension == "xlsx":
        df = pd.read_excel(phones_file)
    
    print(df.iloc[0])


    # Check and new brand exists.

    # Check and add new color.

    # Check and add new Model.

    # Add phones.