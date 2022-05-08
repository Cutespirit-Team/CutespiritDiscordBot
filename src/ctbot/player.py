import asyncio
import discord
import time
import logging
from .playlist import PlayList, PlayListEntry, create_yt_source
from asyncio import Event, Queue, sleep, create_task, ensure_future
# from os import pipe

log = logging.getLogger('ctbot.player')

class SimplePlayer:
    def __init__(self, voice_channel: discord.VoiceChannel=None, playlist: PlayList=None):
        self.voice_channel = voice_channel
        self.voice_client = None

        # self._status_message = None
        self.playlist = playlist or PlayList()
        self._next = Event()
        self._idle = Event()
        self._idle_timer = None
        
    # async def spawn_status_message(self, channel: discord.TextChannel, force: bool=False):
    #     if self._status_message and not force:
    #         await self.update_status_message()
    #         return
    #     if self._status_message:
    #         await self._status_message.delete()
    #     message = await channel.send('< PLACE HOLDER >')
    #     self._status_message = message
    #     await self.update_status_message()

    # async def update_status_message(self):
    #     if self._status_message:
    #         await self._status_message.edit(embed=PlayListPager.get_pagged_list(self.playlist))


    async def on_voice_state_update(self, member, before, after):
        async def leave_when_idle():
            await sleep(60)
            self._idle.set()
            self.voice_client.stop()

        if not self.voice_client.is_connected() or self.voice_client.user.id == member.id:
            return

        if len(self.voice_channel.members) <= 1:
            self.pause(toggle=False)
            log.debug('no audience auto paused')
            self._idle_timer = ensure_future(leave_when_idle())
            log.debug('auto leave timer start')
        else:
            if self._idle_timer:
                log.debug('auto leave timer cancel')
                self._idle_timer.cancel()

            if self.is_paused():
                self.pause(toggle=True)
                log.debug('auto resume')

    async def play(self):
        if self.is_playing():
            return
            
        if not self.voice_client or not self.voice_client.is_connected():
            self.voice_client = await self.voice_channel.connect()
            async def on_voice_state_update_wrapper(*args):
                await self.on_voice_state_update(*args)

            # regist status update event
            self.voice_client.client.on_voice_state_update = on_voice_state_update_wrapper

        self._idle.clear()
        self.playlist.goto(0) # playlist start from first entry
        while not self.playlist.ends() and not self._idle.is_set():
            def finalize(err: discord.ClientException):
                self._next.set()

            self._next.clear()
            source = create_yt_source(self.playlist.upnext())
            self.voice_client.play(source, after=finalize)
            #await self.update_status_message()
            await self._next.wait()
        self.stop()
    
    def stop(self, *, leave: bool=True):
        if self.voice_client and self.voice_client.is_connected():
            self.voice_client.stop()

            if leave:
                create_task(self.voice_client.disconnect())
                # self.voice_client = None
                # if self._status_message:
                #     create_task(self._status_message.delete())

    def pause(self, *, toggle: bool=True):
        if self.is_paused() and toggle:
            self.voice_client.resume()
        else:
            self.voice_client.pause()

    def next(self):
        self.playlist.go_next(force=True)
        create_task(self.stop(leave=False))

    def prev(self):
        self.playlist.go_prev()
        create_task(self.stop(leave=False))

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    def is_paused(self):
        return self.voice_client and self.voice_client.is_paused()
