import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from xml_parser import html_to_xml_parser


def high_volume_screener():
    screener_url = "https://finance.yahoo.com/screener/unsaved/ec58eb86-4029-4e3e-83e0-895ee8dfedc9?offset=0&count=100"
    all_usa_stocks = "https://finance.yahoo.com/screener/unsaved/1e737b26-71fb-402c-859e-805295195484?offset=0&count=100"
    #html = REQUEST(screener_url)
    html = REQUEST(all_usa_stocks)
    xml = html_to_xml_parser(html)

    # xpath_each_rows_details = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]'
    table = xml.findall('.'+'//*[@id="scr-res-table"]/div[1]/table/tbody/tr')

    # get the header from the HTML / XML
    xpath_header = '//*[@id="scr-res-table"]/div[1]/table/thead/tr/th'
    header = xml.findall('.' + xpath_header)

    # get the number of rows from the XML
    xpath_table_elements = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td/'
    #table = xml.findall('.'+xpath_table_elements)

    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[1]/a
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[2]
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[3]
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[4]/span
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[5]
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[6]/span
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[7]
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[8]/span
    # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[9]

    # build dictionary
    quote_format = []
    for column in header:
        text = str(column.text)
        if column.find('a') is not None:
            text = column.find('a').text
        elif column.find('span') is not None:
            text = column.find('span').text
        text = text.replace(' ', '_')
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('%', 'Percent')
        if text != 'None':
            quote_format.append(text)
    print(quote_format)

    quotes = []

    for row in range(0, len(table)-1):
        quote = {}
        for column in range(0, len(table[row].findall('td'))-1):
            text = str(table[row].findall('td')[column].text)
            if table[row].findall('td')[column].find('a') is not None:
                text = table[row].findall('td')[column].find('a').text
            elif table[row].findall('td')[column].find('span') is not None:
                text = table[row].findall('td')[column].find('span').text
            #text = text.replace(' ', '_')
            text = text.replace('(', '')
            text = text.replace(')', '')
            #text = text.replace('%', 'Percent')
            #print(text)
            quote[quote_format[column]] = text
        quotes.append(quote)

    print(quotes)

high_volume_screener()
