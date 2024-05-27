import tabula
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

def string_to_int_if_float(value):
    if is_float(value):
        return int(float(value))
    return None

def remove_carriage_returns(value):
    return value.replace('\r', '')



def format_row(row):
    ro = row[0]
    last = row[1]
    first = row[2]
    year = remove_carriage_returns(row[3])
    make = row[4]
    model = row[5]
    description = '.'.join(row[6:-3])
    date = row[-3]
    v = row[-2]
    invoice = row[-1]
    return [ro, last, first, year, make, model, description, date, v, invoice]


def process(rows):
    table = []
    for row_string in rows:
        row = row_string.split(",")
        if row[0] == 'nan':
            continue

        ro_last = row[0].split(" ")
        if len(ro_last) == 2:
            ro = ro_last[0]
            if ro.isdigit() and int(ro) > 9000:
                last = row[0][len(ro)+1:]
                row[0] = ro
                row[1] = last
                row = format_row(row)
                table.append(row)

        elif len(ro_last) == 1:
            ro_str = ro_last[0]
            ro = 0
            if is_int(ro_str):
                ro = int(ro_str)
            elif is_float(ro_str):
                ro = string_to_int_if_float(ro_str)
            if ro:
                row[0] = ro
                row = format_row(row)
                table.append(row)
        else:
            # Case 3: Check for carrage return
            row = row_string.split("\r")
            print(row)
            if len(row) > 1:
                if is_int(row[1][:5]):
                    ro = int(row[1][:5])
                    if ro > 9000:
                        description = row[1][5:]
                        row2 = [ro, '.', '.', '.', '.', '.', description, '.', '.', '.']
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