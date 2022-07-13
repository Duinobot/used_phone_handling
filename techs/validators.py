import csv

from django.core.exceptions import ValidationError

# used to map csv headers to location fields
HEADERS = {
    'imei': {'field':'imei', 'required':True},
    'C SKU': {'field':'vendor_sku', 'required':True},
    'Manufacturer': {'field':'phonespec__model__brand', 'required':True},
    'Model': {'field':'phonespec__model', 'required':True},
    'Description': {'field':'phonespec__description', 'required':True},
    'Price Inc': {'field':'purchase_price', 'required':True},
    'Storage': {'field':'phonespec__storage', 'required':True},
    'Color': {'field':'phonespec__color', 'required':True},
    'is_locked': {'field':'is_locked', 'required':False},
}

def import_csvfile_validator(csvfile):
    print("entering validator")
    # check file valid csv format
    try:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0, 0)
    except csv.Error:
        raise ValidationError(u'Not a valid CSV file')
    reader = csv.reader(csvfile.read().splitlines(), dialect)
    csv_headers = []
    required_headers = [header_name for header_name, values in
                        HEADERS.items() if values['required']]
    for y_index, row in enumerate(reader):
        # check that all headers are present
        if y_index == 0:
            # store header_names to sanity check required cells later
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_str = ', '.join(missing_headers)
                raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
            continue
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            continue
        # sanity check required cell values
        for x_index, cell_value in enumerate(row):
            # if indexerror, probably an empty cell past the headers col count
            try:
                csv_headers[x_index]
            except IndexError:
                continue
            if csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(u'Missing required value %s for row %s' %
                                            (csv_headers[x_index], y_index + 1))
    return True