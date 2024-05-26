import tabula
import pandas as pd

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def string_to_int_if_float(value):
    if is_float(value):
        return int(float(value))
    return None

def remove_carriage_returns(value):
    return value.replace('\r', '')

def process(rows):
    table = []
    for row_string in rows:
        row = row_string.split(",")
        if row[0] == 'nan':
            continue

        ro_last = row[0].split(" ")
        if len(ro_last) < 2:
            mrow = row[0].split("\r")
            if len(mrow) > 1:
                continue

            ro_str = ro_last[0]
            ro = 0
            if is_int(ro_str):
                ro = int(ro_str)
            elif is_float(ro_str):
                ro = string_to_int_if_float(ro_str)

            if ro:
                last = row[1]
                col_first = row[2]
                col_year = remove_carriage_returns(row[3])
                col_make = row[4]
                col_model = row[5]
                col_description = '.'.join(row[6:-3])
                col_date = row[-3]
                col_v = row[-2]
                col_invoice = row[-1]

                row2 = [ro, last, col_first, col_year, col_make, col_model, col_description, col_date, col_v, col_invoice]
                if len(row2) == 10:
                    table.append(row2)
        else:
            ro = ro_last[0]
            if ro.isdigit() and int(ro) > 9000:
                last = row[0][len(ro)+1:]
                col_first = row[2]
                col_year = remove_carriage_returns(row[3])
                col_make = row[4]
                col_model = row[5]
                col_description = '.'.join(row[6:-3])
                col_date = row[-3]
                col_v = row[-2]
                col_invoice = row[-1]

                row2 = [ro, last, col_first, col_year, col_make, col_model, col_description, col_date, col_v, col_invoice]
                if len(row2) == 10:
                    table.append(row2)
    return table

def to_csv(processed_data):
    if processed_data:
        columns = ['RO', 'Last', 'F', 'Yr', 'Make', 'Model', 'Desc', 'Date', 'Vendor', 'Invoice #']
        processed_df = pd.DataFrame(processed_data, columns=columns)
        processed_df.to_csv("output.csv", index=False)
    else:
        print("No data processed.")

dfs = tabula.read_pdf("sample.pdf", pages='all', multiple_tables=True)
data = []

for df in dfs:
    combined_rows = df.apply(lambda row: ','.join(row.astype(str)), axis=1).tolist()
    table = process(combined_rows)
    if table:
        data.extend(table)

to_csv(data)
