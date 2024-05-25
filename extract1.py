import pandas as pd

def get_sheet(sheet_name):
    sheet = pd.read_csv(sheet_name)
    return sheet



if __name__ == '__main__':
    sheet = get_sheet('output.csv')
    print(sheet)
