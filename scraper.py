import requests
from bs4 import BeautifulSoup
import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\coleg\OneDrive\Documents\MTG\MTG-Python\important_creds.json', scope)
client = gspread.authorize(creds)


def get_price(URL, headers, cardname, foil_status, setname):
    try:
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        content_wrappers = soup.find_all(class_ = 'itemContentWrapper')

        nf_all_wrappers = [a for a in content_wrappers if len(a.find_all(class_ = 'productDetailTitle', string = cardname))>0]

        if foil_status:
            good_wrappers = [a for a in nf_all_wrappers if a.find(class_ = 'foil') != None]
            goodest_wrapper = [a for a in good_wrappers if a.find(class_ = 'productDetailSet').get_text().strip()[:-9] == setname][0]
        elif not foil_status:
            good_wrappers = [a for a in nf_all_wrappers if not a.find(class_ = 'foil') != None]
            goodest_wrapper = [a for a in good_wrappers if a.find(class_ = 'productDetailSet').get_text().strip()[:-4] == setname][0]

        price_raw = goodest_wrapper.find(class_='usdSellPrice').get_text()

        price_clean = float(price_raw[1:len(price_raw)-2] + '.' + price_raw[len(price_raw)-2:])

        return price_clean
    except:
        return float(0)

def send_mail(cardname, foil_status, pricegoal_usd, URL):
    pricegoal_credit = 1.3*pricegoal_usd
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    server.starttls()
    server.ehlo()

    """Sensitive line deleted"""

    subject = cardname + ' is Ready for Buylist!'

    if foil_status:
        body = 'Your FOIL ' + cardname + ' has passed your buylist goal of ' + str(pricegoal_usd) + ' dollars / ' + str(pricegoal_credit) + ' credit! Sell it now!\n' + URL
    else:
        body = 'Your NONFOIL ' + cardname + ' has passed your buylist goal of ' + str(pricegoal_usd) + ' dollars / ' + str(pricegoal_credit) + ' credit! Sell it now!\n' + URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'householdgamingmtg@gmail.com',
        'householdgamingmtg@gmail.com',
        msg
    )
    print('EMAIL SENT')

    server.quit()

def make_URL(cardname):
    adjusted_cardname = cardname.replace(' ', '+')

    URL = 'https://www.cardkingdom.com/purchasing/mtg_singles?filter%5Bsort%5D=price_desc&filter%5Bsearch%5D=mtg_advanced&filter%5Bname%5D=' + adjusted_cardname + '&filter%5Bcategory_id%5D=0&filter%5Bfoil%5D=1&filter%5Bnonfoil%5D=1&filter%5Bprice_op%5D=&filter%5Bprice%5D='

    return URL

def get_requests(starting_row: int):
    read_sheet = client.open('buylist_scraping').worksheet('Cards to Track')

    cardnames = read_sheet.col_values(1)[starting_row:starting_row+40]
    foil_statuses = [a == 'TRUE' for a in read_sheet.col_values(2)[starting_row:starting_row+40]]
    setnames = read_sheet.col_values(3)[starting_row:starting_row+40]
    pricegoals = [float(a) for a in read_sheet.col_values(4)[starting_row:starting_row+40]]

    return[cardnames, foil_statuses, setnames, pricegoals]

def write_data(cardnames, foil_statuses, setnames, prices_usd):
    write_sheet = client.open('buylist_scraping').worksheet('CK Buylist Data') 

    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    for a in range(0, len(cardnames)):

        row = [cardnames[a], foil_statuses[a], setnames[a], prices_usd[a], dt_string]

        index = 1 + len(write_sheet.col_values(1))

        write_sheet.insert_row(row, index)
    
    print(len(cardnames))

    if len(cardnames) < 40:
        return False
    else:
        return True

def main():
    check = True
    count = 0
    starting_row = 1

    while check:
        if count > 0:
            starting_row += 40
            time.sleep(110)
        
        count += 1
        all_data = get_requests(starting_row)

        cardnames = all_data[0]
        foil_statuses = all_data[1]
        setnames = all_data[2]
        pricegoals = all_data[3]

        true_prices = []

        for a in range(0, len(cardnames)):
            cardname = cardnames[a]
            foil_status = foil_statuses[a]
            setname = setnames[a]
            pricegoal_usd = pricegoals[a]
            
            URL = make_URL(cardname)

            price_usd = get_price(URL = URL, headers = headers, cardname = cardname, foil_status = foil_status, setname = setname)
            true_prices.append(price_usd)

            if price_usd >= pricegoal_usd:
                send_mail(cardname = cardname, foil_status = foil_status, pricegoal_usd = pricegoal_usd, URL = URL)
            
        check = write_data(cardnames = cardnames, foil_statuses = foil_statuses, setnames = setnames, prices_usd = true_prices)

if __name__ == "__main__":
    main()
