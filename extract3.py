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
    sheet = pd.read_csv(file_name)
    return sheet

def print_df(df, columns):
    for i in df.index:
        print(df['RO'][i], df['Customer'][i])


def merge_ro(ro):
    payables_rows = []
    # payables_ro = payables.loc[payables['RO'] == ro]
    payables_ro = payables.loc[( payables['RO'] == ro) & (payables['Category '] == 'Sublet') ]
    # print('payables_ro:')
    # print(payables_ro)

    rc_ro = rc_data.loc[rc_data['RO'] == ro]
    # print('rc_ro:')
    # print(rc_ro)

    # print('*******************************')
    pay = pd.merge(payables_ro, rc_ro, on="RO")
    # print(pay)

    sheet_ro = sheet.loc[sheet['RO'] == ro]
    # print('sheet:')
    ro = int(sheet_ro.iloc[0]['RO'])
    date = sheet_ro.iloc[0]['Date']
    customer = sheet_ro.iloc[0]['Customer']
    f   = sheet_ro.iloc[0]['First Initial']
    part = sheet_ro.iloc[0]['Parts NT']

    # payables
    for i in pay.index:
        pay_invoice = pay['Invoice Num'][i]
        pay_date = pay['Date_x'][i]
        pay_cat = pay['Category '][i]              #   Note space
        pay_ven = pay['Vendor_x'][i]
        pay_list = pay['List'][i]
        pay_cost = pay['Cost'][i]
        pay_description = pay['Desc'][i]

        # print(f'{ro}, {date}, {customer}, {f}, {part}, {pay_date}, {pay_invoice}, {pay_cat}, {pay_ven}, {pay_list}, {pay_cost}, {pay_description}')
        row = [ro, date, customer, f, part, pay_date, pay_invoice, pay_cat, pay_ven, pay_list, pay_cost, pay_description]
        payables_rows.append(row)
    return payables_rows


def to_csv(processed_data, columns, file_name):
    if processed_data:
        # Define the column names
        # columns = ['RO', 'Last', 'F', 'Yr', 'Make', 'Model', 'Desc', 'Date', 'Vendor', 'Invoice #']

        # Create a DataFrame from the processed data
        processed_df = pd.DataFrame(processed_data, columns=columns)

        # Save the DataFrame to a CSV file
        processed_df.to_csv(file_name, index=False)
    else:
        print("No data processed.")



if __name__ == '__main__':
    sheet = get_csv('tax_sheet.csv')
    rc_data = get_csv('rc_report.csv')
    payables = get_csv('payables.csv')
    # print(payables.shape)

    sheet_merge = []
    columns = ['RO', 'Date', 'Customer', 'First Initial', 'Parts NT', 'payables_date', 'payables_invoice', 'payables_category', 'payables_vendor', 'payables_list', 'payables_cost', 'description']
    # print(*columns, sep=", ")

    for i in sheet.index:
        ro_float = sheet['RO'][i]
        if is_float(ro_float):
            ro = int(ro_float)
            if ro:
                # print( ro  )
                rows = merge_ro(ro)
                for row in rows:
                    sheet_merge.append(row)

    file_name = 'tax_merge.csv'
    to_csv(sheet_merge, columns, file_name)
