import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from file import READ
from website import Website

from bs4 import BeautifulSoup
from bs4.element import Comment

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# World Stock Market Watch (Quotes + Indices + Currency) (Python)
# by Asher Martin
# Date: October 2022

# IDEAS FOR FURTHER PROJECTS
# TODO setup NLP natural language processing
# TODO setup GUI interface with Python! 

symbols_to_watch = ["pbr", "vale", "intc", "ttm", "goog"]

# Here is the main program that "watches" the internet for me!
def watch():
    time_date()
    #nlp()
    #check_wikipedia_news()
    currencies()
    #world_indices_check()
    """
    for symbol in symbols_to_watch:
        quote(symbol)
    """
    """
    for symbol in symbols_to_watch:
        print("watch calls: ")
        get_option(symbol, "call")
        print("watch puts: ")
        get_option(symbol, "put")
    """

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


# the code orginally came from https://realpython.com/nltk-nlp-python/
def nlp():
    print("Checking Wikipedia News")
    website = "https://en.wikipedia.org/wiki/Portal:Current_events"
    print("loading wikipedia")
    html = get_html(website)
    text = text_from_html(html) #.encode('utf-8', errors='ignore').decode('utf-8')
    sentinces = sent_tokenize(text)
    sentince = word_tokenize(sentinces[0])
    nlp = nltk.pos_tag(sentince)
    print("done with NLP test!")


def quote(symbol):
    stock = {}
    stock["ticker"] = symbol
    stock["date"] = date()
    stock["time"] = time()
    quote_url = "https://finance.yahoo.com/quote/"+symbol
    quate_stats = "https://finance.yahoo.com/quote/" + symbol + "/key-statistics?p=" + symbol
    soup_quote = get_soup(quote_url)
    quotes = soup_quote.select("#quote-summary")[0].find_all('td')
    # typical length of quotes is 32
    # get the stock name
    # #quote-header-info > div.Mt\(15px\).D\(f\).Pos\(r\) > div.D\(ib\).Mt\(-5px\).Maw\(38\%\)--tab768.Maw\(38\%\).Mend\(10px\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1
    stock["name"] = soup_quote.select("#quote-header-info")[0].find_all("h1")[0].text
    stock["price"] = soup_quote.select("#quote-header-info")[0].find_all("fin-streamer")[0].text
    if len(soup_quote.select("#quote-header-info")[0].find_all("fin-streamer")) >= 7:
        stock["after_hours"] = soup_quote.select("#quote-header-info")[0].find_all("fin-streamer")[6].text
    stock["closePrice"] = quotes[1].text
    stock["openPrice"] = quotes[3].text
    stock["bid"] = quotes[5].text.split('x')[0].replace(" ", "")
    stock["bidSize"] = quotes[5].text.split('x')[1].replace(" ", "")
    stock["ask"] = quotes[7].text.split('x')[0].replace(" ", "")
    stock["askSize"] = quotes[7].text.split('x')[1].replace(" ", "")
    stock["dayHigh"] = quotes[9].text.split('-')[1].replace(" ", "")
    stock["dayLow"] = quotes[9].text.split('-')[0].replace(" ", "")
    stock["52High"] = quotes[11].text.split('-')[1].replace(" ", "")
    stock["52Low"] = quotes[11].text.split('-')[0].replace(" ", "")
    stock["volume"] = quotes[13].text.replace(",", "")
    stock["avgVolume"] = quotes[15].text.replace(",", "")
    stock["marketCap"] = quotes[17].text
    stock["beta"] = quotes[19].text
    stock["pe"] = quotes[21].text
    stock["eps"] = quotes[23].text
    stock["earningsDate"] = quotes[25].text
    stock["dividend"] = quotes[27].text.split('(')[0].replace(" ", "")
    stock["yield"] = quotes[27].text.split('(')[1].replace(")", "").replace(" ", "")
    stock["exdifidendDate"] = quotes[29].text
    stock["target"] = quotes[31].text

    #for quote in quotes:
    #    print(quote.text)
    
    #todo soup_stats = get_soup(quate_stats)

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

def get_soup(url):
    html = REQUEST(url)
    return BeautifulSoup(html, 'html.parser')

def get_html(url):
    return REQUEST(url)

# watch a url
def get_xml(url):
    text = REQUEST(url)

    patterns = [r'<[ ]*\![ ]*DOCTYPE.*?>', r'<[ ]*script.*?\/[ ]*script[ ]*>', \
        r'<[ ]*style.*?\/[ ]*style[ ]*>', r'<[ ]*nav.*?\/[ ]*nav[ ]*>', \
            r'<[ ]*\/[ ]*nav[ ]*>', r'<[ ]*form.*?\/[ ]*form[ ]*>', \
                r'<[ ]*footer.*?\/[ ]*footer[ ]*>', r'<[ ]*a class="mw-wiki-logo".*?\/[ ]*a[ ]*>', \
                    r'<[ ]*div id="Overlay.*?\/[ ]*div[ ]*>', r'<[ ]*meta.*?>']

    for pattern in patterns:
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
    soup = get_soup(wikipedia)
    # 
    # CSS selector
    elements = soup.select('#mw-content-text > div.mw-parser-output > div.p-current-events > div.p-current-events-headlines > ul > li')

    for element in elements:
        content = element.text.strip()
        print(content)
        for link in element.find_all('a'):
            print(link["title"])
            print("https://en.wikipedia.org" + link["href"])

def print_sub_trees(tree):
    links = {}
    story = ""
    if tree.text != None:
        print (tree.text, end="")
        if tree.attrib != {}:
            links[tree.attrib["title"]] = "https://en.wikipedia.org" + tree.attrib["href"]
    for sub_tree in tree.findall('.' + "/*"):
        if sub_tree.attrib != {}:
            links[sub_tree.attrib["title"]] = "https://en.wikipedia.org" + sub_tree.attrib["href"]
        links = Merge(links, print_sub_trees(sub_tree))
    if tree.tail != None:
        print (tree.tail, end="")
        if tree.attrib != {}:
            links[tree.attrib["title"]] = "https://en.wikipedia.org" + tree.attrib["href"]
        
    return links

def Merge(dict1, dict2):
    return {**dict1, **dict2}

def currencies():
    print("World Currencies")
    currencies = "https://finance.yahoo.com/currencies/"
    print("checking website: " + currencies)
    soup = get_soup(currencies)
    print ("Website read successfully!")

    world = []
    currency ={}

    #elements = soup.select('#list-res-table > div.Ovx\(a\).Ovx\(h\)--print.Ovy\(h\).W\(100\%\) > table > tbody > tr')
    elements = soup.select("#list-res-table")[0].find_all('tr')
    for element in elements:
        if len(element.select('td')) > 0:
            currency["symbol"] = element.select('td')[0].text
            currency["date"] = date()
            currency["time"] = time()
            currency["name"] = element.select('td')[1].text
            currency["price"] = element.select('td')[2].text
            currency["change"] = element.select('td')[3].text
            currency["pctchange"] = element.select('td')[4].text
        world.append(currency)
        currency = {}
    del world[0]
    print(world)
    return world

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

def date():
    return str(datetime.date.today().strftime("%D"))

def time():
    return str(datetime.datetime.now().strftime("%H:%M:%S"))


#run the program!
watch()
