csv_headers = [
    'year',
    'month',
    'permit_number',
    'applicant_name',
    'site_address',
    'construction_type',
    'contractor',
    'cost_approximate',
    'permit_fee',
    'hookup_fee',
    'outside_city_limits'
]

skiprow_name = [
    'VOID',
    'ROW',
    'ROW/GRADING',
    'ROW (2)',
    'SIGN',
    'GRADING PERMIT',
    'BURN PERMIT',
    'SIGN PERMIT',
    'GRADING',
    'ROW PERMIT',
    'BURN',
    'RIGHT OF WAY PERMIT',
    'SING PERMIT'
]

address_fixes = {
    '14-0253': '1610 COLLEGE',
    '220316': '1996 RUSSELL STREET',
    '220317': '1992 RUSSELL STREET',
    '220318': '1988 RUSSELL STREET',
    '220319': '1984 RUSSELL STREET',
    '220320': '1980 RUSSELL STREET',
    '220500': '2555 CLEAR SPRING ROAD',
    '220204': '2555 CLEAR SPRING ROAD',
    '180140': '2555 CLEAR SPRING ROAD',
    '200744': '2555 CLEAR SPRING ROAD',
    '200253': '2555 CLEAR SPRING ROAD',
    '210541': '1015 CANYON STREET N',
    '15-0463': '407 ST. JOE ST.',
    '230186': '625 WOODLAND DR',
    '15-0385': '1020 N. CANYON',
    '210707': '2555 CLEAR SPRING ROAD',
    '13-0254': '834 AMES STREET',
    '13-0429': '1630 COLLEGE',
    '16-0449': '119 YUKON PL',
    '14-0253': '1630 COLLEGE',
    '230141': '7100 CENTENNIAL RD'
}