# pip install tabula-py

import tabula
import pandas as pd
import re
# import numpy
import math


# Function to split multi-line entries into separate lines
def split_multiline_rows(rows):
    split_rows = []
    for row in rows:
        split_rows.extend(row.split('\r'))
    return split_rows


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
        # Convert the string to a float first
        float_value = float(value)
        # Then convert the float to an integer
        int_value = int(float_value)
        return int_value
    else:
        return None

# Function to remove \r characters from a string
def remove_carriage_returns(value):
    return value.replace('\r', '')


def process(rows):
    # print('***********************')
    # print(rows)
    table = []
    for row_string in rows:
        row = row_string.split(",")
        if row[0] == 'nan':
            year = row[3] * 10
            # print(row)
            continue

        if row[0] != 'nan':
            # print(row)
            ro_last = row[0].split(" ")
            if len(ro_last) < 2:
                mrow = row[0].split("\r")
                if len(mrow) > 1:
                    # print(row)
                    continue


                # print(row)
                # if isinstance(ro_last[0], float):
                # print(type(ro_last[0]))
                # if isinstance(ro_last[0], 'str'):
                # if ro_last[0].isdigit():
                if True:
                    # print(f'******** {ro_last[0]}')
                    ro_str = ro_last[0]
                    ro = 0
                    if is_int(ro_str):
                        ro = int(ro_str)
                    elif is_float(ro_str):
                        ro = string_to_int_if_float(ro_str)
                    


                    # if float(ro) > 9000:
                    if ro:
                        # print('******** 9000')
                        # len_ro = len(ro)
                        last = row[1]
                        num_elements = len(row)
                        col_first = row[2]
                        col_year = remove_carriage_returns(row[3])
                        col_make = row[4]
                        col_model = row[5]
                        col_description = ''
                        for e in row[6:num_elements-3]:
                            col_description += e + "."
                        col_date = row[-3]
                        col_v = row[-2]
                        col_invoice = row[-1]

                        row2 = [ro, last, col_first, col_year, col_make, col_model, col_description, col_date, col_v, col_invoice ]
                        # print(row2)

                        # if ro == '11117':
                        #     print(row)
                        #     print(row2)
                        # data.append(row2)
                        # return row2
                        if len(row2) == 10:
                            table.append(row2)
                            continue

            # print(ro)
            if ro_last[0].isdigit():
                ro = ro_last[0]
                if int(ro) > 9000:
                    len_ro = len(ro)
                    last = row[0][len_ro+1:]
                    num_elements = len(row)
                    col_first = row[2]
                    col_year = remove_carriage_returns(row[3])
                    col_make = row[4]
                    col_model = row[5]
                    col_description = ''
                    for e in row[6:num_elements-3]:
                        col_description += e + "."
                    col_date = row[-3]
                    col_v = row[-2]
                    col_invoice = row[-1]

                    row2 = [ro, last, col_first, col_year, col_make, col_model, col_description, col_date, col_v, col_invoice ]
                    # print(row2)

                    # if ro == '10569':
                    #     print(row)
                    #     print(row2)
                    # data.append(row2)
                    # return row2
                    if len(row2) == 10:
                        table.append(row2)
    return table


def to_csv(processed_data):
    if processed_data:
        # Define the column names
        columns = ['RO', 'Last', 'F', 'Yr', 'Make', 'Model', 'Desc', 'Date', 'Vendor', 'Invoice #']

        # Create a DataFrame from the processed data
        processed_df = pd.DataFrame(processed_data, columns=columns)

        # Save the DataFrame to a CSV file
        processed_df.to_csv("output.csv", index=False)
    else:
        print("No data processed.")



# Read the first page of the PDF file and convert to DataFrame
# dfs = tabula.read_pdf("sample.pdf", pages=5, multiple_tables=True)
dfs = tabula.read_pdf("sample.pdf", pages='all', multiple_tables=True)
# print(dfs)
data = []

for df in dfs:
    # Combine all columns into a single string for each row
    # combined_rows = dfs[0].apply(lambda row: ','.join(row.astype(str)), axis=1).tolist()
    # print('******************** Level 1:')
    combined_rows = df.apply(lambda row: ','.join(row.astype(str)), axis=1).tolist()
    # print(combined_rows)

    # Split multi-line rows into separate lines
    # split_rows = split_multiline_rows(combined_rows)

    # Print split rows for debugging
    # for row in split_rows:
    #     print(row)
    # table = process(split_rows)
    table = process(combined_rows)
    if table:
        print('******************************')
        print(table)
        for row in table:
            data.append(row)

to_csv(data)
