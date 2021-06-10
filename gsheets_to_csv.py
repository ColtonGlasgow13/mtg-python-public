import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os.path
from os import path
import time

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\coleg\OneDrive\Documents\MTG\MTG-Python\important_creds.json', scope)
client = gspread.authorize(creds)

def pull_top50_data(datasource = str):
    read_sheet = client.open('buylist_scraping').worksheet(datasource + ' Data')

    top_50 = [read_sheet.row_values(c) for c in range(2, 52)]

    refined_50 = [x for x in top_50 if x != []]

    return refined_50

def delete_top50_data(datasource = str):
    write_sheet = client.open('buylist_scraping').worksheet(datasource + ' Data')

    for c in reversed(range(2, 52)):
        write_sheet.delete_row(c)

def store_data(top_50, datasource = str) -> bool:
    """
    returns True if file is not empty yet, and False if it is.
    """
    #dataframe so can use normal indexing
    top50_df = pd.DataFrame.from_records(top_50)

    top50_df.columns = ['cardname', 'foil_status', 'setname', 'price_usd', 'time']

    for ind in top50_df.index:
        if top50_df['foil_status'][ind] == 'TRUE':
            foil = 'Foil'
        elif top50_df['foil_status'][ind] == 'FALSE':
            foil = 'Nonfoil'

        if not path.exists(datasource + ' Data\\'+ top50_df['cardname'][ind] + '_' + foil + '_' + top50_df['setname'][ind] + '.csv'):
            top50_df.iloc[[ind]].transpose().transpose().to_csv(datasource + ' Data\\'+ top50_df['cardname'][ind] + '_' + foil + '_' + top50_df['setname'][ind] + '.csv', index=False)
        else:
            top50_df.iloc[[ind]].transpose().transpose().to_csv(datasource + ' Data\\'+ top50_df['cardname'][ind] + '_' + foil + '_' + top50_df['setname'][ind] + '.csv', index=False, mode = 'a', header=False)
        
    if len(top50_df.index) < 50:
        return False
    elif len(top50_df.index) == 50:
        return True


def main():
    check = True
    count = 0
    while check:
        if count > 0:
            time.sleep(110)
        
        data = pull_top50_data('CK Buylist')

        delete_top50_data('CK Buylist')

        check = store_data(data, 'CK Buylist')
        count += 1

    
    print('Cycled ' + str(count) + ' times!')


if __name__ == "__main__":
    main()