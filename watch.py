import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from file import READ
from website import Website

# World Stock Market Watch (Quotes + Indices + Currency) (Python)
# by Asher Martin
# Date: July 2020

# url = "https://www.google.com/search?q=INDEXSP:.INX"
# url = "https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC"
# url = "https://finance.yahoo.com/quote/PBR?p=PBR&.tsrc=fin-srch"
# url = "https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch"
# xpath_google_quote = './/*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span'

symbols_to_watch = ["ttm", "tsla", "msft", "googl"]
symbols_to_watch = ["chu", "ytra", "pbr"]
symbols_to_watch = ["pbr", "vale"]

def watch():
    time_date()
    for symbol in symbols_to_watch:
        quote(symbol)
    currency_check()
    world_indices_check()
"""
    for symbol in symbols_to_watch:
        print("watch calls: ")
        get_option(symbol, "call")
        print("watch puts: ")
        get_option(symbol, "put")
"""



def quote(symbol):
    quote_url = "https://finance.yahoo.com/quote/"+symbol
    quate_stats = "https://finance.yahoo.com/quote/" + symbol + "/key-statistics?p=" + symbol
    xml = get_xml(quote_url)
    xml_stats = get_xml(quate_stats)
    xpath_name = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1'
    xpath_price = '//*[@id="quote-header-info"]/div[3]/div/div/span[1]'
    xpath_bid = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/'
    xpath_ask = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/'
    xpath_volume = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span'
    xpath_avg_volume = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span'
    xpath_market_cap = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span'
    xpath_day_range = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]'
    xpath_52_week_range = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]'
    xpath_pe_ratio = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]/span'
    xpath_close = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span'
    xpath_open = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span'
    xpath_beta = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span'
    xpath_dividend_yield = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[7]/td[2]/span'
    xpath_eps = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]/span'
    xpath_earnings_date = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]/span'
    xpaths = {"name" : xpath_name, "price" : xpath_price, "bid" : xpath_bid, "bid_volume" : xpath_bid, "ask" : xpath_ask, "ask_volume" : xpath_ask,"volume" : xpath_volume, "avg_volume" : xpath_avg_volume, \
        "market_cap" : xpath_market_cap, "day_range" : xpath_day_range, "year_range" : xpath_52_week_range, "eps" : xpath_eps, "earnings_date" : xpath_earnings_date, \
        "pe_ratio" : xpath_pe_ratio, "previous_close" : xpath_close, "open" : xpath_open, "beta" : xpath_beta, "dividend_yield" : xpath_dividend_yield}
    
    clock = datetime.datetime.now()
    #milliseconds = str(clock.time())
    time = clock.time().strftime('%H:%M:%S')
    date = str(datetime.date.today().strftime("%B")) + " " \
          + str(datetime.date.today().strftime("%d")) + ", " \
          + str(datetime.date.today().strftime("%Y"))
    stock = {"ticker" : symbol, "date" : date, "time" : time}
    for xpath in xpaths:
        if xml.find('.' + xpaths[xpath]) != None:
            text = xml.find('.' + xpaths[xpath]).text
            if text != None:
                if re.sub("[^\d\.\-]", "", text) != '':
                    # check for market cap case (b or m) (add later if it has a m you need to "mill")
                    # check for bid/ask
                    if xpath == "bid" or xpath == "bid_volume":
                        xsplit = re.split("x",xml.find('.' + xpaths[xpath]).text)
                        stock["bid"] = float(re.sub("[^\d\.\-]", "", xsplit[0]))
                        stock["bid_volume"] = float(re.sub("[^\d\.\-]", "", xsplit[1]))
                    elif xpath == "ask" or xpath == "ask_volume":
                        xsplit = re.split("x",xml.find('.' + xpaths[xpath]).text)
                        stock["ask"] = float(re.sub("[^\d\.\-]", "", xsplit[0]))
                        stock["ask_volume"] = float(re.sub("[^\d\.\-]", "", xsplit[1]))
                    elif xpath == "day_range":
                        stock["day_range"] = xml.find('.' + xpath_day_range).text
                    elif xpath == "year_range":
                        stock["year_range"] = xml.find('.' + xpath_52_week_range).text
                    elif xpath == "dividend_yield":
                        stock["dividend_yield"] = xml.find('.' + xpath_dividend_yield).text
                    elif xpath == "name":
                        stock["name"] = text
                    else: 
                        stock[xpath] = float(re.sub("[^\d\.\-]", "", xml.find('.' + xpaths[xpath]).text))
    print(stock)

def buy(stock):
    print ("buy")

def sell(stock):
    print ("sel")

def get_option(symbol, call_or_put):
    quote_url = "https://finance.yahoo.com/quote/" + symbol + "/options?straddle=false"
    xml = get_xml(quote_url)
    option = {}
    if call_or_put == "call":
        section = "1"
    elif call_or_put == "put":
        section = "2"
    else:
        print("error: call_or_put option type not specified!")
        return
    # count the number of "rows" in the call or put table
    xpath_table = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr'
    table_rows = len(xml.findall('.' + xpath_table))
    for row in range(1, table_rows+1):
        xpath_contract_name = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[1]/a'
        contract_name = xml.find('.' + xpath_contract_name).text
        option["contract_name"] = contract_name
        xpath_trade_date = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[2]'
        trade_date = xml.find('.' + xpath_trade_date).text
        option["trade_date"] = trade_date
        xpath_strike_price = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[3]/a'
        strike_price = xml.find('.' + xpath_strike_price).text
        option["strike_price"] = float(strike_price.replace(",",""))
        xpath_last_price = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[4]'
        last_price = xml.find('.' + xpath_last_price).text
        option["last_price"] =  float(last_price.replace(",",""))
        xpath_bid = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[5]'
        bid = xml.find('.' + xpath_bid).text
        if len(bid) > 1:
            option["bid"] = float(bid.replace(",",""))
        else:
            option["bid"] = 0.0
        xpath_ask = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[6]'
        ask = xml.find('.' + xpath_ask).text
        if len(ask) > 1:
            option["ask"] =  float(ask.replace(",",""))
        else:
            option["ask"] = 0.0
        xpath_change = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[7]/span'
        change = xml.find('.' + xpath_change).text
        option["change"] =  float(change)
        xpath_percent_change = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[8]/span'
        percent_change = xml.find('.' + xpath_percent_change).text
        if len(percent_change) > 1:
            option["percent_change"] =  float(percent_change.replace("%",""))
        else: 
            option["percent_change"] =  0.0
        xpath_volume = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[9]'
        volume = xml.find('.' + xpath_volume).text
        if volume.isnumeric():
            option["volume"] = int(volume.replace(",","").replace(",",""))
        else:
            option["volume"] = 0
        xpath_open_interest = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[10]'
        open_interest = xml.find('.' + xpath_open_interest).text
        if open_interest.isnumeric():
            option["open_interest"] = int(open_interest.replace(",",""))
        else:
            option["open_interest"] = 0
        xpath_implied_volatility = '//*[@id="Col1-1-OptionContracts-Proxy"]/section/section[' + section + ']/div[2]/div/table/tbody/tr[' + str(row) +']/td[11]'
        implied_volatility = xml.find('.' + xpath_implied_volatility).text
        option["implied_volatility"] = float(implied_volatility.replace(",","").replace("%",""))
        print (option)
    
def log(item):
    # save data to log file (csv)
    print("log.txt")

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
