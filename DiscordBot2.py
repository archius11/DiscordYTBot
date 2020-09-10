import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl
import subprocess
import random

import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# os.system('set PATH=%PATH%;E:\\ffmpeg\\bin')

bot = commands.Bot(command_prefix='$')

audioPlayers = {}
guilds = {}

z_tracks = {
    0: 'tracks\\z\\2 минуты на размышление.mp3',
    1: 'tracks\\z\\да не дамажте вы господи.mp3',
    2: 'tracks\\z\\дефолтная хуйня жми сейв.mp3',
    3: 'tracks\\z\\единственный баг это твое рождение.mp3',
    4: 'tracks\\z\\попроси не диспелить 10 раз уже вайпнулись на залупе.mp3',
    5: 'tracks\\z\\пранкеры, может я нахуй пойду посижу пока вы не выучите тактику.mp3',
    6: 'tracks\\z\\пришли подпсить спасибо РО.mp3',
    7: 'tracks\\z\\сова по фамилии меркель некем заменить будем говно жрать тем кто есть.mp3',
    8: 'tracks\\z\\стоит афк хтт быстрина.mp3',
    9: 'tracks\\z\\топ 2000 дпс поты он не пьет.mp3',
    10: 'tracks\\z\\трамп президент профессионалы высочайшего класса.mp3',
    11: 'tracks\\Directed by Robert B. Weide- theme meme.mp3',
    12: 'tracks\\z\\enia.mp3'
}


class GuildClient:
    def __init__(self, guild):
        self.guild = guild
        self.bot_member = guild.me
        self.audio_player = AudioPlayer2(self)

    def _voice_channel_required(func):  # функция
        async def wrapper(*args, **kwargs):  # обёртка wrapper
            guild_client = args[0]
            voicechannel = guild_client.getVoiceChannel()
            if voicechannel is None:
                await guild_client.sendTextMessage('join the bot before the command');
            else:
                await func(*args, **kwargs)

        return wrapper

    async def check_text_channel(self):
        channel_name = 'youtube-player'
        existing_channel = discord.utils.get(self.guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await self.guild.create_text_channel(channel_name)

    async def on_ready(self):
        print(f'{bot.user.name} has connected to Discord!' + str(self.guild))

        for guild in bot.guilds:
            channel_name = 'youtube-player'
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if not existing_channel:
                print(f'Creating a new channel: {channel_name}')
                await guild.create_text_channel(channel_name)

    async def join(self, ctx):
        author = ctx.author
        channel = author.voice.channel
        await channel.connect()

    async def exit(self):
        server = self.guild.voice_client
        if server:
            await server.disconnect(force=True)

    @_voice_channel_required
    async def play(self, url=''):
        await self.audio_player.addTrack(url)

    @_voice_channel_required
    async def stop(self):
        await self.audio_player.stopTrack()

    async def queue(self):
        await self.audio_player.printQueue()

    @_voice_channel_required
    async def next(self):
        await self.audio_player.nextTrack()

    @_voice_channel_required
    async def back(self):
        await self.audio_player.previousTrack()

    async def clear(self):
        await self.audio_player.clearQueue()

    @_voice_channel_required
    async def pause(self):
        await self.audio_player.pausePlay()

    @_voice_channel_required
    async def resume(self):
        await self.audio_player.resumePlay()

    @_voice_channel_required
    async def playlist(self, url):
        await self.audio_player.loadPlaylist(url)

    @_voice_channel_required
    async def playZ(self, num):
        if num == -1:
            num = random.randrange(len(z_tracks))
        await self.audio_player.playmp3(num)

    async def textzz(self):
        txt = '\n'.join([f" $z {i}: {z_tracks[i]}" for i in z_tracks])
        await self.sendTextMessage(str(txt))

    async def sendTextMessage(self, msg):
        channel = await self.getTextChannel()
        await channel.send(msg)

    async def getTextChannel(self):
        channel_name = 'youtube-player'
        existing_channel = discord.utils.get(self.guild.channels, name=channel_name)
        if not existing_channel:
            raise None
        return existing_channel

    def getVoiceChannel(self):
        if self.bot_member.voice is None:
            return None
        else:
            return self.bot_member.voice.channel

    async def change_channel(self, member, before, after):
        pass
        # if self.itiswowguild(self):
        #     update_romanticpairtstats()

    # #
    # async def periodic_actions(self):
    #     if not self.itiswowguild():
    #         return
    #     print('periodic')
    #     if self.itiswowguild():
    #         ch = self.romanticpair()
    #         if not ch == False:
    #             await self.setromanticmusic(ch)
    #     return
    #
    # def itiswowguild(self):
    #     return self.guild.name == 'Minutoid server'
    #     return self.guild.name == 'И так сойдет'
    #
    # def romanticpair(self):
    #     if not self.audio_player.stopped:
    #         return
    #     channels = self.guild.voice_channels
    #     member_kailit = discord.utils.get(self.guild.members, discriminator='4199')
    #     member_polina = discord.utils.get(self.guild.members, discriminator='4737')
    #     member_archie = discord.utils.get(self.guild.members, discriminator='3408')
    #     member_tasha = discord.utils.get(self.guild.members, discriminator='8427')
    #     for channel in channels:
    #         # if len(channel.members) == 2 and \
    #         #         member_archie in channel.members and \
    #         #         member_tasha in channel.members:
    #         if len(channel.members) >= 1 and \
    #                 member_archie in channel.members:
    #             return channel
    #     return False
    #
    # async def setromanticmusic(self, channel):
    #     print('before channel')
    #     if not channel:
    #         return
    #     ch = self.getVoiceChannel()
    #     if not ch:
    #         print('before connected')
    #         try:
    #             voice = await channel.connect()
    #             print('after connect')
    #         except:
    #             pass
    #
    #         print('connected')
    #         return
    #     else:
    #         await self.exit()
    #         print('exit')
    #         return
    #     print('url')
    #     musicurl = 'https://www.youtube.com/watch?v=3ZayGR8OWvI'
    #     return
    #     # voice = discord.utils.get(bot.voice_clients, guild=self.guild)
    #     # if voice and voice.is_connected():
    #     #     await voice.move_to(channel)
    #     # else:
    #     if not ch:
    #         voice = await channel.connect()
    #     await self.audio_player.addTrack(musicurl, True)
    #     # await guild.play(musicurl)


class AudioTrack:
    def __init__(self, url):
        self.url = url
        self.title = ''

    def __repr__(self):
        if self.title:
            return self.title
        else:
            return self.url


class AudioPlayer2:
    def __init__(self, guild_client):
        self.playlist = []
        self.currentTrack = None
        self.guild_client = guild_client
        self.stopped = True
        self.paused = False

    async def playTrack(self):
        current = self.currentTrack
        if not current:
            return

        channel = self.guild_client.getVoiceChannel()
        if not channel:
            return
        voice = discord.utils.get(bot.voice_clients, guild=self.guild_client.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'outtmpl': '%(id)s'  # .%(ext)s',
        # }

        # url = 'https://www.youtube.com/watch?v=Oblbsp9zHp8'

        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     file = ydl.extract_info(current.url, download=True)
        # path = str(file['id'])  # + ".webm")
        # current.title = file.get('title', current.url)
        # source = await discord.FFmpegOpusAudio.from_probe(path)
        # self.currentTrack = current
        # if voice.is_playing():
        #     voice.stop()
        # voice.play(source, after=self.nextTrack) #after=lambda x: self.nextTrack)

        voice.stop()
        audiostreamprocess = subprocess.Popen(["python3.8", "/home/admin/code/discord_yt_bot/DiscordYTBot/audiostream.py", current.url], stdout=subprocess.PIPE)
        # source = discord.FFmpegPCMAudio(audiostreamprocess.stdout, pipe=True, stderr=audiostreamprocess.stderr)
        source = await self.getAudioSource(audiostreamprocess)
        voice.play(source, after=lambda x: self.nextTracksync(x))
        await self.guild_client.sendTextMessage(str(self.currentTrack) + ' is playing')

    async def playmp3(self, num):
        channel = self.guild_client.getVoiceChannel()
        if not channel:
            return
        voice = discord.utils.get(bot.voice_clients, guild=self.guild_client.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        voice.stop()
        source = await discord.FFmpegOpusAudio.from_probe(z_tracks[num])
        if voice.is_playing():
            voice.stop()
        voice.play(source)

    async def getAudioSource(self, audiostreamprocess):
        return discord.FFmpegPCMAudio(audiostreamprocess.stdout, pipe=True, stderr=audiostreamprocess.stderr)

    async def addTrack(self, url, silent=False):
        if url:
            self.playlist.append(AudioTrack(url))
            if not silent:
                await self.guild_client.sendTextMessage(f'Track added to queue ({len(self.playlist)} /'
                                                        f'total). !queue to list ')

        if self.currentTrack is None:
            self.setCurrentTrack(index=0)

        if not url:
            if self.currentTrack is not None:
                await self.playTrack()
                return
            else:
                return

        if self.stopped:
            self.stopped = False
            self.paused = False
            await self.nextTrack()
            return
        if self.paused:
            await self.resumePlay()
            return

    async def stopTrack(self):
        self.stopped = True
        channel = self.guild_client.getVoiceChannel()
        if not channel:
            return
        voice = discord.utils.get(bot.voice_clients, guild=self.guild_client.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        voice.stop()

    async def printQueue(self):
        msglist = ["Queue:"]
        for i in self.playlist:
            txt = ''
            if i.title:
                txt += i.title  # + ' (' + i.url + ')'
            else:
                txt += i.url
            txt += '                                <-- Playing now' if i == self.currentTrack else ''
            msglist.append(txt)

        l2 = list(zip(*[iter(msglist)] * 5))
        if len(msglist) % 5 > 0:
            l2.append(msglist[-(len(msglist) % 5):])
        for i in l2:
            txt = '\n'.join(i)
            await self.guild_client.sendTextMessage(txt)

    async def previousTrack(self):
        if self.stopped:
            return
        if not self.playlist:
            return
        res = self.setCurrentTrack(moveto=-1)
        if not res:
            self.currentTrack = None
            return
        await self.playTrack()

    def nextTracksync(self, x=None):
        if self.currentTrack not in self.playlist or \
                self.playlist.index(self.currentTrack) == len(self.playlist) - 1:
            return

        try:
            fut = asyncio.run_coroutine_threadsafe(self.nextTrack(), bot.loop)
            fut.result()
        except Exception as e:
            print(e)

    async def nextTrack(self):
        if self.stopped:
            return
        # Если бот в войс канале - тогда играем там
        # Если бот не в войс канале - тогда стоп
        if not self.playlist:
            return
        res = self.setCurrentTrack(moveto=1)
        if not res:
            self.currentTrack = None
            return
        await self.playTrack()

    def setCurrentTrack(self, **kwargs):
        if len(self.playlist) == 0:
            return False
        if 'index' in kwargs:
            index = kwargs['index']
            index = max(index, 0)
            index = min(index, len(self.playlist) - 1)
            self.currentTrack = self.playlist[index]
            return True

        if 'moveto' in kwargs:
            moveto = kwargs['moveto']
            if self.currentTrack is not None:
                try:
                    index = self.playlist.index(self.currentTrack)
                except ValueError:
                    index = 0
            else:
                index = 0
            index += moveto
            index = max(index, 0)
            index = min(index, len(self.playlist) - 1)
            self.currentTrack = self.playlist[index]
            return True
        return False

    async def clearQueue(self):
        self.playlist = []

    async def pausePlay(self):
        channel = self.guild_client.getVoiceChannel()
        if not channel:
            return
        voice = discord.utils.get(bot.voice_clients, guild=self.guild_client.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if voice.is_playing():
            self.paused = True
            voice.pause()

    async def resumePlay(self):
        channel = self.guild_client.getVoiceChannel()
        if not channel:
            return
        voice = discord.utils.get(bot.voice_clients, guild=self.guild_client.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if not voice.is_playing() and self.paused:
            self.paused = False
            voice.resume()

    async def loadPlaylist(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extract_flat': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=False)

        ytlist = file.get('entries', None)

        if not ytlist:
            return

        for i in ytlist:
            video_id = i['id']
            currenturl = 'https://www.youtube.com/watch?v=' + video_id
            await self.addTrack(currenturl, True)
            self.playlist[-1].title = i.get('title', '')

        await self.guild_client.sendTextMessage(f'Added {str(len(ytlist))} tracks to queue')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        guilds[guild] = GuildClient(guild)
        await guilds[guild].check_text_channel()
    print(f'{len(bot.guilds)} guilds today')


# @bot.event
# async def on_error(event, *args, **kwargs):
#     print(f'some error here')
#

# @bot.event
# async def on_voice_state_update(member, before, after):
#     guild_client = guilds[after.channel.guild]
#     await guild_client.change_channel(member, before, after)


@bot.command(pass_context=True, brief="Makes the bot join your channel", name='join')
async def join(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.join(ctx)


@bot.command(pass_context=True, brief="Makes the bot leave your channel", name='exit')
async def exit(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.exit()


@bot.command(pass_context=True, brief="Plays audio from Youtube link", name='play')
async def play(ctx, url=''):
    guild_client = guilds[ctx.message.guild]
    await guild_client.play(url)


@bot.command(pass_context=True, brief="Stop playing music", name='stop')
async def stop(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.stop()


@bot.command(pass_context=True, brief="List of tracks", name='queue')
async def queue(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.queue()


@bot.command(pass_context=True, brief="Play next track", name='next')
async def next(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.next()


@bot.command(pass_context=True, brief="Play previous track", name='back')
async def back(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.back()


@bot.command(pass_context=True, brief="Clear queue", name='clear')
async def clear(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.clear()


@bot.command(pass_context=True, brief="Pause playing", name='pause')
async def pause(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.pause()


@bot.command(pass_context=True, brief="Resume playing", name='resume')
async def resume(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.resume()


@bot.command(pass_context=True, brief="Resume playing", name='playlist')
async def playlist(ctx, url):
    guild_client = guilds[ctx.message.guild]
    await guild_client.playlist(url)

@bot.command(pass_context=True, brief="Resume playing", name='z')
async def z(ctx, num=-1):
    guild_client = guilds[ctx.message.guild]
    await guild_client.playZ(num)

@bot.command(pass_context=True, brief="Resume playing", name='zz')
async def zz(ctx):
    guild_client = guilds[ctx.message.guild]
    await guild_client.textzz()


def start_bot():
    print('starting bot')
    bot.run(TOKEN)


if __name__ == '__main__':
    start_bot()
