import json


def write_quote(symbol, quote):
    with open(symbol + '.json', 'w') as outfile:
        json.dump(quote, outfile)


def read_quote(symbol):
    with open(symbol + '.json') as json_file:
        data = json.load(json_file)
