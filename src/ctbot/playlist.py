import time
from enum import Enum
from discord import FFmpegPCMAudio
from urllib.request import urlopen
from .ytdl import YTDL

def is_downloadable(url: str):
    try:
        resp = urlopen(url)
    except Exception as e: # 
        # TODO： delete this once fully tested
        print(f"{__name__}: ytdl code 403 occure")
        return False
    return True

class LoopMode(Enum):
    NORMAL = 0,
    LIST = 1,
    SINGLE = 2,

class PlayListEntry:
    def __init__(self, uri: str, discriminator: str, lazy: bool=True):
        self.uri = uri
        self.discriminator = discriminator
        self._touchat = 0
        self._bad = False

        if not lazy:
            self.load_info()
    
    def load_info(self) -> bool:
        if self.cache_avaiable() and is_downloadable(self.url):
            return True

        for _ in range(5):
            try:
                info = YTDL.fetch(self.uri)
                if is_downloadable(info.get('url')):
                    break
            except Exception as e:
                # TODO: log
                print('[Error] while interact with youtube.\n\n', e)
        else:
            return False

        self.id = info.get('id', None)
        self.title = info.get('title', '<No Title>')
        self.url = info.get('url', None)
        self.thumbnail = info.get('thumbnail', None)
        self.webpage = info.get('webpage_url', None)
        self.duration = info.get('duration', 0)
        self._touchat = time.time()
        return True

    def cache_avaiable(self):
        # cache at least 60 minutes
        return (time.time() - self._touchat) < (60 * 60) 

class PlayList:
    def __init__(self, *, name: str='Unnamed', loop_mode: LoopMode=LoopMode.NORMAL):
        self.name = name
        self.loop_mode = loop_mode
        self._list = []
        self._index = 0
    
    def add_entry(self, uri: str, discriminator: str=''):
        # TODO: handle playlist
        self._list.append(PlayListEntry(uri, discriminator))

    def get_entries(self):
        # NOTE: should it return a copy ???
        return self._list

    def clear_entries(self):
        self._list = []

    def goto(self, index):
        self._index = min(0, max(index, len(self._list) - 1))

    def ends(self):
        return len(self._list) == 0 or self._index >= len(self._list)

    def upnext(self):
        if self.ends():
            return None
        upnext = self._list[self._index]
        self.go_next()
        return upnext

    def go_next(self, *, force: bool=False):
        if force:
            if self.loop_mode == LoopMode.SINGLE: 
                self._index += 1
            return
        
        if self.loop_mode == LoopMode.NORMAL:
            self._index += 1
        elif self.loop_mode == LoopMode.LIST:
            self._index = (self._index + 1) % len(self._list)

    def go_prev(self):
        self._index = max(0, self._index - 2)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
def create_yt_source(entry):
    ok = entry.load_info()
    return FFmpegPCMAudio(entry.url, **FFMPEG_OPTIONS)


# class PlayListPager:
#     @classmethod
#     def get_pagged_list(cls, playlist: PlayList, page: int=None, item_per_page: int=9):
#         current_index = max(0, playlist._index - 1)
#         total_pages = math.ceil(len(playlist.get_entries()) / item_per_page)
#         current_page = page or (current_index // item_per_page)
#         embed = discord.Embed(title='', color=0xffffd5)
#         paging_info = '[{}] {}/{} pages'.format(current_index + 1, current_page + 1, total_pages)
#         embed.add_field(name='Title', value=paging_info, inline=False)
#         start, end = (current_page * item_per_page), min((current_page + 1) * item_per_page, len(playlist.get_entries()))
#         for i in range(start, end):
#             entry = playlist.get_entries()[i]
#             err = entry.fetch_info() # TODO: put this to background 
#             name = '{}, #{}'.format(i+1, entry.discriminator)
#             if i % 9 == current_index % 9:
#                 name += '  :notes:'

#             prep = {}
#             if entry._bad:
#                 name += '  :x:'
#                 prep = {
#                     'uri': entry.uri,
#                     'title': '<Fail to load>'
#                 }
#             else:
#                 prep = {
#                     'uri': entry.uri,
#                     'title': truncate(entry.title[0])
#                 }
#             embed.add_field(name=name, value='[{title}](https://youtube.com/watch?v={uri})'.format(**prep), inline=True)

#         #time.strftime('%H:%M:%S', time.gmtime(12345))
#         #bar = '{} {} {}'.format('00:00', process_bar(20, width=72), '00:00')
#         #embed.add_field(name='', value='', inline=False)
#         return embed

