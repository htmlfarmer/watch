import urllib.request
from file import READ
from file import WRITE


# REQUEST(address)
# DETAILS: gets the HTML from any website address
from urllib.error import HTTPError

def REQUEST(address):
    try:
        req = urllib.request.Request(address)
        req.add_header('User-Agent', 'RESEARCH (LINUX; Pacific North West, USA)')
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:  # Checking if page exists
            html = response.read().decode('utf-8')  # Decoding response
            return html
        else:
            print("Page not found")
            return None
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# REQUEST(address, filename, directory)
# DETAILS: gets the HTML from any website and saves it to a file and directory
# if the filename is None or "" then the address is used
# if the directory is None or "" then the default directory is "./"


def REQUEST_FILE(address, **kwargs):
    directory = kwargs["directory"]
    filename = kwargs["filename"]
    if filename is None:
        filename = address
        filename = filename.replace('/', '_')
    if directory is None:
        directory = "./"
    html = READ(filename, directory)
    if html is None:
        html = REQUEST(address)
        print("REQUEST (ONLINE): " + address)
        WRITE(filename, directory, html)
    else:
        print("REQUEST   (FILE): " + address)
    return html
