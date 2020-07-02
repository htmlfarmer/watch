import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from file import READ
from website import Website

# World Stock Market Watch (Quotes + Indices + Currency) (Python)
# by Asher Martin

# url = "https://www.google.com/search?q=INDEXSP:.INX"
# url = "https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC"
# url = "https://finance.yahoo.com/quote/PBR?p=PBR&.tsrc=fin-srch"
# url = "https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch"
# xpath_google_quote = './/*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span'


def watch():
    time_date()
    currency_check()
    world_indices_check()
    stock_quote("SP500")


def stock_quote(stock):
    quote_url = "https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC"
    xml = get_xml(quote_url)
    xpath_quote = '//*[@id="quote-header-info"]/div[3]/div/div/span[1]'
    quote = xml.find('.' + xpath_quote).text
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    quote = locale.atof(quote)
    print(stock + " = " + str(quote))

# return the value at a given xpath
def xpath_text(website, xpath):
    path = website.xml.find("." + xpath)
    if path.text:
        return path.text
    else:
        return None

# watch a url
def get_xml(url):
    text = REQUEST(url)

    # (REMOVE <SCRIPT> to </script> and variations)
    pattern = r'<[ ]*script.*?\/[ ]*script[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML <STYLE> to </style> and variations)
    pattern = r'<[ ]*style.*?\/[ ]*style[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML <META> to </meta> and variations)
    pattern = r'<[ ]*meta.*?>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML COMMENTS <!-- to --> and variations)
    pattern = r'<[ ]*!--.*?--[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML DOCTYPE <!DOCTYPE html to > and variations)
    pattern = r'<[ ]*\![ ]*DOCTYPE.*?>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # for some reason & is not a valid char in XML parse
    text = text.replace('&', '&amp;')

    # HTML/XML is now "clean" so we can create an binary XML tree
    parser = ElementTree.XMLParser(encoding="utf-8")
    xml = ElementTree.fromstring(text, parser=parser)
    return xml


def currency_check():
    print("World Currencies")
    currencies = "https://finance.yahoo.com/currencies/"
    print("checking website: " + currencies)
    xml = get_xml(currencies)
    xpath_currencies = {"EURUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[3]/td[3]',
                        "CNYUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[16]/td[3]',
                        "INRUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[19]/td[3]',
                        "GBPUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[5]/td[3]',
                        "MYRUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[24]/td[3]',
                        "JPYUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[4]/td[3]',
                        "GBPUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[5]/td[3]',
                        "MXNUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[20]/td[3]',
                        "PHPUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[21]/td[3]',
                        "RUBUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[26]/td[3]',
                        "IDRUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[22]/td[3]',
                        "THBUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[23]/td[3]',
                        "ZARUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[25]/td[3]',
                        "CHFUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[13]/td[3]',
                        "SGDUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[18]/td[3]',
                        "HKDUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[17]/td[3]',
                        "NZDUSD": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[7]/td[3]'}

    for currency in xpath_currencies:
        quote = xml.find('.' + xpath_currencies[currency]).text
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        quote = locale.atof(quote)
        # NAME = '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[4]/td[1]/a'
        # PRICE = '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[4]/td[3]',
        print(currency + " = $" + str(quote))


def world_indices_check():
    # WORLD INDICES
    print("World Stock Market Indices")
    indices = "https://finance.yahoo.com/world-indices"
    print("checking: " + indices)
    xml = get_xml(indices)
    xpath_indices = {"USA SP500 (^GSPC)": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[1]/td[3]',
                     "Brazil (IBOVESPA ^BVSP)": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[30]/td[3]',
                     "Mexico (IPC ^MXX)": '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[30]/td[3]',
                     "India (BSE SENSEX ^BSESN)" : '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[23]/td[3]',
                     "Germany (DAX ^GDAXI)" : '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[10]/td[3]'
                     }

    for index in xpath_indices:
        quote = xml.find('.' + xpath_indices[index]).text
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        quote = locale.atof(quote)
        # NAME = '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[4]/td[1]/a'
        # PRICE = '//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr[4]/td[3]',
        print(index + " = $" + str(quote))


# print a header showing all the details of when the transaction takes place
def time_date():
    print("===================================================")
    print("    TIME # " + str(datetime.datetime.now()))
    print("    DATE : " + str(datetime.date.today().strftime("%B")) + " " \
          + str(datetime.date.today().strftime("%d")) + ", " \
          + str(datetime.date.today().strftime("%Y")))
    print("===================================================")


#run the program!
watch()
