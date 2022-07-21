import openpyxl
import pandas as pd

from django.core.exceptions import ValidationError

# used to map csv headers to location fields
HEADERS = [
    'IMEI',
    'C SKU',
    'Manufacturer',
    'Model',
    'Description',
    'Price Inc',
    'Color',
]

def import_csvfile_validator(phones_file):
    print("entering validator")
    print(phones_file)
    if phones_file.name.split(".")[-1].lower() == 'csv':
        df = pd.read_csv(phones_file.open())
        df = df.rename(columns=lambda x: x.strip())
        file_header = str(df.columns.values)
        for header in HEADERS:
            try:
                header in file_header
            except:
                raise ValidationError(u'Missing: %s' % (header) + "." + " Required: 'IMEI, C SKU, Manufacturer, Model, Description, Price Inc, Color'")

    if phones_file.name.split(".")[-1].lower() == 'xlsx':
        print(phones_file.name.split(".")[-1].lower())
        wb = openpyxl.load_workbook(phones_file)
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        file_header = next(rows)
        for header in HEADERS:
            try:
                file_header.index(header)
            except:
                raise ValidationError(u'Missing: %s' % (header) + "." + " Required: 'IMEI, C SKU, Manufacturer, Model, Description, Price Inc, Color, Storage'")

    return True