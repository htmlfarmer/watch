import xml.etree.ElementTree as ElementTree
from request import REQUEST_FILE

class Website:
    def __init__(self):
        self.url =  None  # web address
        self.html = None  # HTML is text
        self.xml = None  # XML ElementTree
        self.filename = None  # filename to be saved
        self.directory = None  # directory to save file in

    def get_url(self):
        return self.url

    def get_html(self):
        if self.html is None:
            self.html = REQUEST_FILE(self.get_url(), filename=self.get_filename(), directory=self.get_directory())
        return self.html

    def get_xml(self):
        if self.xml is None:
            self.xml = ElementTree.fromstring(self.get_html())
        return self.xml

    def get_filename(self):
        return self.filename

    def get_directory(self):
        if self.directory is None:
            self.directory = "./"
        return self.directory

    def set_filename(self, filename):
        self.filename = filename

    def set_directory(self, directory):
        self.directory = directory

    def set_xml(self, text):
        self.xml = ElementTree.fromstring(text)
        self.html = None

    def set_html(self, text):
        self.html = text
        self.xml = None  # reset the XML

    def set_url(self, url):
        self.url = url
        self.html = None  # reset the html
        self.xml = None   # reset the xml
        self.filename = None  # reset the filename
        self.directory = None
