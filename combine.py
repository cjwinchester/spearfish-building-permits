from glob import glob
import csv

from scourgify import normalize_address_record

from const import skiprow_name, address_fixes, csv_headers


data_files_in = glob('data/*.csv')
filepath_out = 'spearfish-building-permits.csv'

# a list to hold the processes data
combined_data = []

# loop over the CSV files
for file in data_files_in:

    # open the file
    with open(file, 'r') as infile:
        data = list(csv.DictReader(infile))
    
    # loop over the rows of data
    for row in data:

        permit_id = row.get('permit_number').replace('/', '-')

        # list of fields to upcase and nuke whitespace
        fields_standardize = [
            'applicant_name',
            'site_address',
            'construction_type',
            'contractor'
        ]

        for field in fields_standardize:
            row[field] = ' '.join(
                row[field].upper().split()
            )

        # skip permits for signs, burns, grading, etc.
        if row['applicant_name'] in skiprow_name:
            combined_data.append(row)
            continue

        # validate: coerce cost estimates to float
        # but return w/ 2 decimals
        if row['cost_approximate']:
            row['cost_approximate'] = '{:.2f}'.format(
                float(row['cost_approximate'])
            )

        # handle permit fees
        permit_fee = row['permit_fee']

        if permit_fee:
            if permit_fee.lower() == 'waived':
                row['permit_fee'] = ''
            else:
                row['permit_fee'] = '{:.2f}'.format(
                    float(permit_fee.replace(',', ''))
                )

        # and make the hookup fees floats
        if row['hookup_fee']:
            row['hookup_fee'] = '{:.2f}'.format(
                float(row['hookup_fee'])
            )

        address = row['site_address']

        # validate address formatting
        address_to_parse = address_fixes.get(
            permit_id,
            address
        )

        # check for a common parsing mistake
        if address_to_parse[0].isalpha():
            raise Exception(f'Check the address for {permit_id} ({file})\n    {address}')

        normalize_address_record(f'{address_to_parse} Spearfish, SD')

        combined_data.append(row)

# sort desc by year, month, project cost
combined_data.sort(
    key=lambda row: (
        row.get('year'),
        row.get('month'),
        float(row.get('cost_approximate') or 0)
    ),
    reverse=True
)

with open(filepath_out, 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(combined_data)

    print(f'Wrote {len(combined_data):,} permit records to file: {filepath_out}')
