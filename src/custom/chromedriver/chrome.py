from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os
import time

from configparser import ConfigParser

import glob

WINDOW_SIZE = "1440,900"

credentials_path = os.getcwd() + '/prim_login.ini'

download_directory = os.getcwd() + '/data/'

class Chrome:
    def __init__(self):
        try:
            # read credentials file
            parser = ConfigParser()
            parser.read(credentials_path)

            section="login"
            filename="prim_login.ini"

            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    match param[0]:
                        case 'username':
                            self.username = os.environ.get(param[1])
                        case 'password':
                            self.password = os.environ.get(param[1])
                        case 'api_jeton':
                            self.my_api_jeton = os.environ.get(param[1])
            else:
                raise Exception('Section {0} not found in the {1} file'.format(section, filename))

            #self._connect()
        except:
            print('no credentials found')

    def _connect(self,url_connection):
        self.url_connection = url_connection
        options = webdriver.ChromeOptions()
        path_download_pref = {'download.default_directory' : download_directory}
        options.add_experimental_option("prefs",path_download_pref)
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # print("starting webdriver ...")
        self.web = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
        self.web.set_page_load_timeout(60)  #added to prevent from endless connection attempts
        self._login()

    def _login(self):
        # print("start loging...")
        self.get_url(self.url_connection)
        self.send_keys('input[@id="username"]', self.username)
        self.send_keys('input[@id="id-pwd"]', self.password)
        # Button "Me connecter" to click for connection
        self.web.find_element("xpath",'/html/body/div/main/section[1]/form/div/p/input').click()

    def get_url(self, url):
        self.web.get(url)
        #time.sleep(5)

    def send_keys(self, element, string):
        textbox = self.web.find_element("xpath",'//' + element)
        textbox.send_keys(string)

    def click(self, element):
        clickable_element = self.web.find_element("xpath",'//' + element)
        clickable_element.click()
    
    def download_wait(self,directory, timeout, nfiles=None):
        """
        Wait for downloads to finish with a specified timeout.

        Args
        ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        nfiles : int, defaults to None
            If provided, also wait for the expected number of files.

        """
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            os.chdir(directory)
            files = glob.glob("*.csv*")
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1
        return seconds