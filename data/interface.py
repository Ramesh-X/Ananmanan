from .states import *
from .consts import *
from .data_loader import DataLoader


class Interface(object):

    def __init__(self):
        self.__data_loader = DataLoader('./downloads')
        self.__state = NO_STATE
        self.__cmds = []
        self.__page_id = 1

    def __print_initial_msg(self, cmd='none'):
        print("Welcome to Anammanan Downloader..\nEnter your commands below...\n")
        print("Anytime, if you want to go back enter 99 and if you want to start from the beginning enter 999..")
        print("Also you can exit the software by typing quit...")
        print("Do you need to search by:\n\t1) Song Name\n\t2) Artist Name\n\t3) Custom search")
        print("Please enter a number below")
        self.__state = INITIAL_STATE

    def __handle_back(self, cmd, func, hard_back=False):
        if (not hard_back) and self.__state != INITIAL_STATE:
            self.__cmds.pop()
        if cmd == '999':
            self.__cmds = []
            self.__print_initial_msg()
        elif cmd == '99':
            func(self.__cmds.pop())
        else:
            print('Invalid character (%s). Please try again' % cmd)

    def __search(self, cmd: str):
        if cmd in '1)':
            print("Enter the first letter of the name of the song")
            self.__state = SEARCH_SONG_BY_NAME
        elif cmd in '2)':
            print("Enter the first letter of the name of the artist")
            self.__state = SEARCH_SONG_BY_ARTIST
        elif cmd in '3)':
            print("Enter the custom search string you want")
            # To Do: Give options to search by commands eg: regex
            self.__state = SEARCH_CUSTOM
        else:
            self.__handle_back(cmd, self.__print_initial_msg)

    def __show_results_name(self, cmd):
        item_list = self.__data_loader.get_name_list_from(cmd, self.__page_id)
        if item_list is None:
            if self.__page_id == 1:
                print("There is no song starts with the given character %s", cmd)
                self.__handle_back('99', self.__search, True)
                return
            print('The given id is not valid. Starting from the beginning')
            self.__page_id = 1
            name_list, page_info = self.__data_loader.get_name_list_from(cmd, self.__page_id)
        name_list, page_info = item_list
        print('\n'.join(['%d) %s [downloads: %d]' % (item['index'], item['name'], item['count']) for item in name_list]))
        print(page_info)
        print('\nEnter nn to goto next page. pp to previous page. id<num> to goto page given by <num>.')
        print('To select a song type sel<num> to download the song given by <num> in the list')

    def __name_c_entered(self, cmd: str):
        if cmd in first_chrs:
            self.__page_id = 1
            self.__state = NAME_CHR_ENTERED
            self.__show_results_name(cmd)
        else:
            self.__handle_back(cmd, self.__search)

    def __name_results(self, cmd: str):
        show_result = True
        if cmd == 'nn':
            self.__cmds.pop()
            cmd = self.__cmds[-1]
            self.__page_id += 1
        elif cmd == 'pp':
            self.__cmds.pop()
            cmd = self.__cmds[-1]
            self.__page_id -= 1
            if self.__page_id < 1:
                self.__page_id = 1
        elif cmd.startswith('id'):
            try:
                self.__page_id = int(cmd[2:])
            except:
                print("Cannot identify a ID given. Going back to the beginning..")
                self.__page_id = 1
            self.__cmds.pop()
            cmd = self.__cmds[-1]
        elif cmd.startswith('sel'):
            pass
        else:
            show_result = False
            self.__handle_back(cmd, self.__search)
        if show_result:
            self.__show_results_name(cmd)

    def __custom_search(self, cmd: str):
        if cmd == 'url':
            self.__state = URL_BASED_CUSTOM
        elif cmd == 'all':
            self.__state = ALL_DOWN_CUSTOM
        else:
            self.__handle_back(cmd, self.__search)

    def __custom_url_based(self, cmd: str):
        args = cmd.split()
        if len(args) < 2:
            print("Format\nurl d<num>")
            self.__handle_back(cmd, self.__custom_search)
        url = args[0]
        args = args[1:]
        if not url.startswith('http://www.ananmanan.lk/free-sinhala-mp3'):
            print("URL given is not valid. Enter again")
            return
        count_lim = 0
        for arg in args:
            if arg.startswith('d'):
                try:
                    count_lim = int(arg[1:])
                except:
                    print('error number format. Try again as d<num>')
                    return
        if count_lim == 0:
            print("Downloading all songs..")
        item_list = self.__data_loader.get_name_list_from_url(url)
        if item_list is None:
            print('Some Error')
            return
        name_list, _ = item_list
        for item in name_list:
            if item['count'] > count_lim:
                print("downloading item: '%s' with %d downloads" % (item['name'], item['count']))
                self.__data_loader.download_file_from_id(item['id'], '%s.mp3' % item['name'])
                
    def __custom_all_download(self, cmd: str):
        try:
            count_lim = int(cmd)
        except:
            print("Enter the minimum download count. If need to download all enter 0")
            return
        i = 0
        while True:
            i += 1
            item_list = self.__data_loader.get_name_list_from_all(i)
            if item_list is None:
                print("Program stopped downloading songs in page", i)
                return
            name_list, _ = item_list
            for item in name_list:
                if item['count'] > count_lim:
                    print("downloading item: '%s' with %d downloads" % (item['name'], item['count']))
                    self.__data_loader.download_file_from_id(item['id'], '%s.mp3' % item['name'])
        

    def __redirect_to_function(self, cmd: str):
        cmd = cmd.strip()
        if cmd is None or cmd == '':
            return
        if self.__state == NO_STATE:
            self.__print_initial_msg()
        elif self.__state == INITIAL_STATE:
            self.__search(cmd)
        elif self.__state == SEARCH_SONG_BY_NAME:
            self.__name_c_entered(cmd)
        elif self.__state == NAME_CHR_ENTERED:
            self.__name_results(cmd)
        elif self.__state == SEARCH_CUSTOM:
            self.__custom_search(cmd)
        elif self.__state == URL_BASED_CUSTOM:
            self.__custom_url_based(cmd)
        elif self.__state == ALL_DOWN_CUSTOM:
            self.__custom_all_download(cmd)

    def begin(self):
        cmd = 'initial'
        while cmd not in ['exit', 'quit', 'close']:
            self.__redirect_to_function(cmd)
            cmd = input('> ').lower()
            self.__cmds.append(cmd)
