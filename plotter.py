import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def read_data(cardname: str, foil_status:str, setname:str, datasource:str) -> list:
    """
    Reads requested data from computer and returns a dataframe of price and time
    """
    with open(datasource + ' Data\\'+ cardname + '_' + foil_status + '_' + setname + '.csv') as d:
        df = pd.read_csv(d)

    price_time_df = df[['price_usd', 'time']]

    return price_time_df


def plotter(df, cardname, foil_status, setname, datasource):
    """
    Takes a dataframe of price and time
    """
    df.time=pd.to_datetime(df.time)
    df.plot('time', 'price_usd')

    plt.xlabel('Date')
    plt.ylabel('Price USD')
    plt.ylim(0, max(df['price_usd'])*1.15)
    plt.title(datasource + ' Data, ' + foil_status + ' ' + cardname + ', ' + setname)
    plt.show()


def main():
    cardname = input('Cardname? ')
    foil_status = input("Foil? (First Letter Capital, rest lowercase) ")
    setname = input('Setname? ')
    datasource = input('Data Source? ')

    df = read_data(cardname, foil_status, setname, datasource)
    plotter(df, cardname, foil_status, setname, datasource)

if __name__ == "__main__":
    main()