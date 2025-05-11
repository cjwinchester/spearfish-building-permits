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
            continue

        # validate: coerce cost estimates to float
        # but return w/ 2 decimals
        if row['cost_approximate'] and row['cost_approximate'] != "-":
            row['cost_approximate'] = '{:.2f}'.format(
                float(row['cost_approximate'])
            )

        # handle permit fees
        permit_fee = row['permit_fee']

        if permit_fee:
            if permit_fee.lower() == 'waived' or permit_fee == "-":
                row['permit_fee'] = ''
            else:
                row['permit_fee'] = '{:.2f}'.format(
                    float(permit_fee.replace(',', ''))
                )

        # and make the hookup fees floats
        if row['hookup_fee']:
            row['hookup_fee'] = '{:.2f}'.format(
                float(row['hookup_fee'].replace('‐', '') or 0)
            )

        address = row['site_address']

        # some manual lookups
        address_to_parse = address_fixes.get(
            permit_id,
            address
        )

        # check for a common parsing mistake
        if address_to_parse[0].isalpha():
            raise Exception(f'Check the address for {permit_id} ({file})\n    {address}')

        # clean/validate address
        city = 'SPEARFISH'
        state = ' SD '
        zipcode = '57783'

        city = city if city not in address_to_parse else ''
        state = state.strip() if state not in address_to_parse else ''
        zipcode = zipcode if zipcode not in address_to_parse else ''

        add_to_address = ' '.join([city, state, zipcode]).strip()

        address = f'{address_to_parse} {add_to_address}'.strip()

        # don't need to keep city/state/zipcode returned
        # here because implied, just checking address format
        try:
            normalize_address_record(address)
        except:
            print(f'Check the address for {permit_id} ({file})\n    {address}')

        combined_data.append(row)

# sort desc by year, month, project cost
combined_data.sort(
    key=lambda row: (
        row.get('year'),
        row.get('month'),
        row.get('cost_approximate', 0)
    ),
    reverse=True
)

with open(filepath_out, 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(combined_data)

    print(f'Wrote {len(combined_data):,} permit records to file: {filepath_out}')
