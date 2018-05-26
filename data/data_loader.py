import urllib.request as urllib2
from bs4 import BeautifulSoup
from .consts import *
import shutil
from urllib.error import URLError
import os


class DataLoader(object):

    def __init__(self, download_dir: str):
        page = urllib2.urlopen(base_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        soup.prettify()
        self.__soup = soup
        self.__download_dir = download_dir

    def set_soup(self, url: str):
        try:
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page, 'html.parser')
            soup.prettify()
            self.__soup = soup
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        except Exception as e:
            print("Error Occurred. Reason:\n", e)

    def __download_file(self, url: str, file_name: str):
        file_name = '%s/%s' % (self.__download_dir, file_name)
        if os.path.isfile(file_name):
            print("File already there.. Going to next :)")
            return
        try:
            with urllib2.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        except IOError as e:
            print("Error while accessing file\nReason:", e.strerror)

    def download_file_from_id(self, id: str, file_name: str):
        self.__download_file(download_url % id, file_name)

    def get_name_list_from(self, c: str, pid: int=1):
        url = song_by_name % (c, pid)
        return self.get_name_list_from_url(url, False)

    def get_name_list_from_url(self, url: str, any: bool=True):
        self.set_soup(url)
        head = self.__soup.find(id='content').h1.text
        if (not any) and (song_page_heading not in head):
            return None
        song_list = self.__soup.find(id='content').find_all('div', class_='mp3')
        name_list = []
        for i, song in enumerate(song_list):
            values = {
                'index': int(i),
                'name': song.a.text,
                'id': int(song.a.get('href').split('/')[3]),
                'count': int(song.find_all('span', class_='downlodcount')[0].text[1:-2].replace(',', ''))
            }
            name_list.append(values)
        pagen = self.__soup.find_all('div', class_='pagenavi2')
        if not pagen:
            pagen = 'Single Page Output'
        else:
            pagen = pagen[0].text
        return name_list, pagen

