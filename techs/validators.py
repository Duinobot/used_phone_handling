from csv import DictReader
from io import TextIOWrapper
import openpyxl

from django.core.exceptions import ValidationError

# used to map csv headers to location fields
HEADERS = {
    'IMEI',
    'C SKU',
    'Manufacturer',
    'Model',
    'Description',
    'Price Inc',
    'Color',
    'Storage'
}

def import_csvfile_validator(phones_file):
    print("entering validator")
    print(phones_file)
    if phones_file.name.split(".")[-1].lower() == 'csv':
        rows = TextIOWrapper(phones_file, encoding="utf-8", newline="")
        file_header = list(map(str.strip, rows.readline().split(",")))
        for header in HEADERS:
            try:
                file_header.index(header)
            except:
                raise ValidationError(u'Missing: %s' % (header) + "." + " Required: 'IMEI, C SKU, Manufacturer, Model, Description, Price Inc, Color, Storage'")

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