import youtube_dl as yt

class YTDL:
    YTDL_OPTIONS = {'format': 'bestaudio', 'extract_flat': True}
    #YTDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    @classmethod
    def fetch(cls, q: str):
        ytdl = yt.YoutubeDL(cls.YTDL_OPTIONS)
        return ytdl.extract_info(q, download=False)
