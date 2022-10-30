import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from file import READ
from website import Website

# World Stock Market Watch (Quotes + Indices + Currency) (Python)
# by Asher Martin
# Date: October 2022

# IDEAS FOR FURTHER PROJECTS
# TODO setup NLP natural language processing
# TODO setup GUI interface with Python! 

# url = "https://www.google.com/search?q=INDEXSP:.INX"
# url = "https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC"
# url = "https://finance.yahoo.com/quote/PBR?p=PBR&.tsrc=fin-srch"
# url = "https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch"
# xpath_google_quote = './/*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/span[1]/span/span'

symbols_to_watch = ["ttm", "tsla", "msft", "googl"]
symbols_to_watch = ["chu", "ytra", "pbr"]
symbols_to_watch = ["pbr", "vale"]

# Here is the main program that "watches" the internet for me!
def watch():
    time_date()
    check_wikipedia_news()
    
    # note doesn't work because I added remove nav and remove footer code for wikipedia
    #currency_check()
    #world_indices_check()
    
    """
    for symbol in symbols_to_watch:
        quote(symbol)

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

    # (REMOVE HTML <NAV> to </nav> and variations)
    pattern = r'<[ ]*nav.*?\/[ ]*nav[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE </nav> and variations for some reason I have some that remain!?)
    pattern = r'<[ ]*\/[ ]*nav[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML <NAV> to </nav> and variations)
    pattern = r'<[ ]*form.*?\/[ ]*form[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # (REMOVE HTML <footer> to </footer> and variations)
    pattern = r'<[ ]*footer.*?\/[ ]*footer[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # for some reason wikipedia has a bug in the XML code
    # (REMOVE HTML <a class="mw-wiki-logo> to </a> and variations)
    pattern = r'<[ ]*a class="mw-wiki-logo".*?\/[ ]*a[ ]*>'  # mach any char zero or more times
    text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

    # <div id="Overlay-2-Empty-Proxy" data-reactroot="">
    pattern = r'<[ ]*div id="Overlay.*?\/[ ]*div[ ]*>'  # mach any char zero or more times
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

    # for some reason some XML files have \n's in them and too long lines!
    text = text.replace('\n', '')
    text = text.replace('\t', '')

    # HTML/XML is now "clean" so we can create an binary XML tree
    parser = ElementTree.XMLParser(encoding="utf-8")
    xml = ElementTree.fromstring(text, parser=parser)
    return xml

def check_wikipedia_news():
    print("Checking Wikipedia News")
    wikipedia = "https://en.wikipedia.org/wiki/Portal:Current_events"
    print("loading wikipedia")
    xml = get_xml(wikipedia) #note there is a bug when parsing the wikipedia pages!
    print("recieved!")
    xpath_latest_news = '//*[@id="mw-content-text"]/div[1]/div[2]/div[4]/ul'
    news_tree = xml.findall('.' + xpath_latest_news + "/*")
    for story in news_tree:
        links = print_sub_trees(story)
        print ("")
        print (links)


def print_sub_trees(tree):
    links = {}
    story = ""
    if tree.text != None:
        print (tree.text, end="")
        if tree.attrib != {}:
            links[tree.attrib["title"]] = "https://en.wikipedia.org" + tree.attrib["href"]
    for sub_tree in tree.findall('.' + "/*"):
        print_sub_trees(sub_tree)
        if sub_tree.attrib != {}:
            links[sub_tree.attrib["title"]] = "https://en.wikipedia.org" + sub_tree.attrib["href"]
    if tree.tail != None:
        print (tree.tail, end="")
        if tree.attrib != {}:
            links[tree.attrib["title"]] = "https://en.wikipedia.org" + tree.attrib["href"]
        
    return links
        
# check currency on yahoo!
def currency_check():
    print("World Currencies")
    currencies = "https://finance.yahoo.com/currencies/"
    print("checking website: " + currencies)
    xml = get_xml(currencies)
    print ("Website read successfully!")

    # this code should read all the headers and then print the header!
    xpath_labels = '//*[@id="list-res-table"]/div[1]/table/thead/tr/th'

    # count the number of "rows" in the call or put table
    xpath_table = '//*[@id="list-res-table"]/div[1]/table/tbody/tr'
    table_rows = len(xml.findall('.' + xpath_table))

    xml_table(xpath_labels, xpath_table, xml)

def xml_table(xpath_table_header, xpath_table_body, xml):

    # this code should read all the headers and then print the header!
    xpath_table_header = '//*[@id="list-res-table"]/div[1]/table/thead/tr/th'
    table_colums = len(xml.findall('.' + xpath_table_header))
    labels = xml.findall('.' + xpath_table_header)
    header = []
    for label in labels: 
        header.append(label.text) 
    print (header)

    # count the number of "rows" in the call or put table
    # todo add the code to search for the name of the body of the table.
    #end = xpath_table_header.rfind("tr/")
    #xpath_table = xpath_table_header[:end+2]
    #table_rows = len(xml.findall('.' + xpath_table))

    # print each label for each row
    table_rows = len(xml.findall('.' + xpath_table_body))
    for row in range(1, table_rows+1):
        for element in range(0, len(header)):
            xpath_name = '//*[@id="list-res-table"]/div[1]/table/tbody/tr['+ str(row) +']/td['+ str(element+1) +']'

            # first //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a 
            if xml.find('.' + xpath_name).text != None:
                print (xml.find('.' + xpath_name).text)
            else: 
                children = xml.findall('.' + xpath_name + "/*")
                while children:
                    for child in children:
                        if child.text != None:
                            print (child.text)
                            children = None
                            break
                        elif child.tag != None:
                            xpath_name += "/" + child.tag
                            children = xml.findall('.' + xpath_name + "/*")
                        else:
                            break 

            """
            if xml.find('.' + xpath_name).text != None:
                name = xml.find('.' + xpath_name).text
                print (header[element] + " " + name)
                # //*[@id="list-res-table"]/div[1]/table/tbody/tr[2]/td[1]/a
                # //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a
                # //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[3]/fin-streamer
                # //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[5]/fin-streamer/span
            elif xml.find('.' + xpath_name + "/fin-streamer").text != None:
                name = xml.find('.' + xpath_name + "/fin-streamer").text
                print (header[element] + " " + name)
            """
            # //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[3]/fin-streamer //*[@id="list-res-table"]/div[1]/table/tbody/tr[1]/td[4]/fin-streamer/span

def world_indices_check():
    # WORLD INDICES
    print("World Stock Market Indices")
    indices = "https://finance.yahoo.com/world-indices"
    print("checking: " + indices)
    xml = get_xml(indices)
    print("Web Page Read (Success!)")

    # count the number of "rows" in the call or put table
    xpath_table = '//*[@id="list-res-table"]/div[1]/table/tbody/tr'
    table_rows = len(xml.findall('.' + xpath_table))

    # print each label for each row
    for row in range(1, table_rows+1):
        xpath_symbol = '//*[@id="list-res-table"]/div[1]/table/tbody/tr['+ str(row) +']/td[1]/a'
        symbol = xml.find('.' + xpath_symbol).text
        xpath_name = '//*[@id="list-res-table"]/div[1]/table/tbody/tr['+ str(row) +']/td[2]'
        name = xml.find('.' + xpath_name).text
        xpath_price = '//*[@id="list-res-table"]/div[1]/table/tbody/tr['+ str(row) +']/td[3]/fin-streamer'
        price = xml.find('.' + xpath_price).text
        print (name + " (" + symbol + ") : " + price)


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
