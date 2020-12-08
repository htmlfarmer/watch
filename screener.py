import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from xml_parser import html_to_xml_parser

screener_url = "https://finance.yahoo.com/screener/unsaved/ec58eb86-4029-4e3e-83e0-895ee8dfedc9?offset=0&count=100"
all_usa_stocks = "https://finance.yahoo.com/screener/060813e7-8061-4068-821f-8ba5865e1eb0?offset=0&count=100"


# page 2 https://finance.yahoo.com/screener/unsaved/1e737b26-71fb-402c-859e-805295195484?count=100&offset=100

def main():
    download_yahoo_screener(all_usa_stocks)


def download_yahoo_screener(url):
    html = REQUEST(url)
    xml = html_to_xml_parser(html)
    screened = yahoo_volume_screener(xml)
    number_screened = int(xml.find('.' + '//*[@id="screener-criteria"]/div[2]/div[1]/div[2]/div/div[2]/div').text)
    index = 0
    index = index + 100
    while index < number_screened:
        url = url[0:url.find("?")] + "offset=" + str(index) + "&count=100"
        # first index of ? or /
        html = REQUEST(url)
        xml = html_to_xml_parser(html)
        screened.append(yahoo_volume_screener(xml))
        index = index + 100
    return screened


def yahoo_volume_screener(xml):
    # xpath_each_rows_details = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]'
    table = xml.findall('.' + '//*[@id="scr-res-table"]/div[1]/table/tbody/tr')

    # get the header from the HTML / XML
    xpath_header = '//*[@id="scr-res-table"]/div[1]/table/thead/tr/th'
    header = xml.findall('.' + xpath_header)

    # get the number of rows from the XML
    xpath_table_elements = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td/'
    # table = xml.findall('.'+xpath_table_elements)

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

    for row in range(0, len(table)):
        quote = {}
        for column in range(0, len(table[row].findall('td')) - 1):
            text = str(table[row].findall('td')[column].text)
            if table[row].findall('td')[column].find('a') is not None:
                text = table[row].findall('td')[column].find('a').text
            elif table[row].findall('td')[column].find('span') is not None:
                text = table[row].findall('td')[column].find('span').text
            # text = text.replace(' ', '_')
            text = text.replace(',', '')
            text = text.replace('(', '')
            text = text.replace(')', '')
            text = text.replace('%', '')
            text = text.replace('+', '')
            if len(text) > 2:
                if text[-2].isdigit():
                    if text[-1] == "M":
                        text = text.replace('.', '')
                        text = text.replace('M', '')
                        text = text + "000"
                    if text[-1] == "B":
                        text = text.replace('.', '')
                        text = text.replace('B', '')
                        text = text + "000000"
                    if text[-1] == "T":
                        text = text.replace('.', '')
                        text = text.replace('T', '')
                        text = text + "000000000"
                # print(text)
            if (text.replace('.', '', 1).replace('-', '', 1).isdigit()):
                quote[quote_format[column]] = float(text)
            else:
                quote[quote_format[column]] = text
        quotes.append(quote)

    return quotes


main()
