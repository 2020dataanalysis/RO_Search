import pandas as pd
import math

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        x = float(value)
        if math.isnan(x):
            return False
        return True
    except ValueError:
        return False

def get_csv(file_name):
    return pd.read_csv(file_name)

def merge_ro(ro, payables, rc_data, sheet):
    payables_rows = []
    payables_ro = payables.loc[(payables['RO'] == ro) & (payables['Category '] == 'Sublet')]
    rc_ro = rc_data.loc[rc_data['RO'] == ro]
    pay = pd.merge(payables_ro, rc_ro, on="RO")

    sheet_ro = sheet.loc[sheet['RO'] == ro].iloc[0]
    ro = int(sheet_ro['RO'])
    date = sheet_ro['Date']
    customer = sheet_ro['Customer']
    first_initial = sheet_ro['First Initial']
    parts_nt = sheet_ro['Parts NT']

    for i in pay.index:
        pay_invoice = pay['Invoice Num'][i]
        pay_date = pay['Date_x'][i]
        pay_cat = pay['Category '][i]  # Note the space in 'Category '
        pay_vendor = pay['Vendor_x'][i]
        pay_list = pay['List'][i]
        pay_cost = pay['Cost'][i]
        pay_description = pay['Desc'][i]

        row = [ro, date, customer, first_initial, parts_nt, pay_date, pay_invoice, pay_cat, pay_vendor, pay_list, pay_cost, pay_description]
        payables_rows.append(row)
    return payables_rows

def to_csv(processed_data, columns, file_name):
    if processed_data:
        processed_df = pd.DataFrame(processed_data, columns=columns)
        processed_df.to_csv(file_name, index=False)
    else:
        print("No data processed.")

if __name__ == '__main__':
    sheet = get_csv('tax_sheet.csv')
    rc_data = get_csv('rc_report.csv')
    payables = get_csv('payables.csv')

    sheet_merge = []
    columns = ['RO', 'Date', 'Customer', 'First Initial', 'Parts NT', 'payables_date', 'payables_invoice', 'payables_category', 'payables_vendor', 'payables_list', 'payables_cost', 'description']

    for i in sheet.index:
        ro_float = sheet['RO'][i]
        if is_float(ro_float):
            ro = int(ro_float)
            if ro:
                rows = merge_ro(ro, payables, rc_data, sheet)
                sheet_merge.extend(rows)

    file_name = 'tax_merge.csv'
    to_csv(sheet_merge, columns, file_name)
