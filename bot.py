import os
import mod

from random import choice
from dotenv import load_dotenv
from os.path import join
from twitchio import Chatter
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
CHANNELS = mod.get_channel()
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_NICK = os.environ.get('BOT_NICK')

bot = commands.Bot(
    prefix=PREFIX,
    token=TOKEN,
    initial_channels=CHANNELS
)

client = Client(
    token=TOKEN
)


@bot.event()
async def event_ready():
    print("ta on crl")


@bot.event()
async def event_message(message):
    marinaetc = ['marina43Etcetera', 'marina43Love',
                 'marina43Oclinhos', 'marina43Reza', 'marina43Trail', 'marina43Testalol', 'marina43Gatilh']
    CHANNEL = message.channel.name
    msg = message.content
    content = msg.split()
    autor = message.author.name
    time = message.timestamp.strftime('%H:%M:%S')
    print(f'#{CHANNEL} {time} {autor}: {msg}')
    if CHANNEL == 'marinaetc':
        if autor != '1bode':
            if set(content) & set(marinaetc):
                await message.channel.send(f'{choice(marinaetc)}')


@bot.command(name='bode')
async def bode(ctx):
    if ctx.channel.name == 'xumartins1':
        await ctx.channel.send('👀')
    elif ctx.channel.name == 'bodedotexe':
        await ctx.channel.whisper(f'tiamo nini marina43Love')


@bot.command(name='namorado', aliases=['namorada','namo'])
async def namorado(ctx):
    if ctx.channel.name == 'marinaetc':
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])
        if namo != '':
            try:
                value = int(list(mod.get("@all", 'marinaetc').keys())[-1])+1
            except IndexError:
                value = 1
            input = {value: namo}
            mod.add(input, 'marinaetc')
            await ctx.channel.send(f'/me {ctx.author.name} -> {namo} adicionado à lista de namorados da marinaetc.')
            return
        else:
            await ctx.channel.send(f'/me {ctx.author.name} -> Adicione o nome do namorado após o comando')
    elif ctx.channel.name == 'emylolz':
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])
        if namo != '':
            try:
                value = int(list(mod.get("@all", 'emylolz').keys())[-1])+1
            except IndexError:
                value = 1
            input = {value: namo}
            mod.add(input, 'emylolz')
            await ctx.channel.send(f'/me {ctx.author.name} -> {namo} adicionada à lista de namoradas da emy.')
            return
        else:
            await ctx.channel.send(f'/me {ctx.author.name} -> Adicione o nome da namorada após o comando')


@bot.command(name='divorcio')
async def divorcio(ctx):
    if ctx.channel.name == 'marinaetc':
        message = ctx.message.content
        if Chatter.is_mod or ctx.author == 'bodedotexe':
            namo = ' '.join(message.split()[1:])
            if namo != '':
                try:
                    if mod.get(namo, 'marinaetc') != None:
                        try:
                            while mod.delcmd(namo, 'marinaetc') != None:
                                await ctx.channel.send(f'/me {ctx.author.name} -> Marina Reticências divorciou-se de {namo}.')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.channel.send(f'/me {ctx.author.name} -> Namorado não encontradokkkk')
    elif ctx.channel.name == 'emylolz':
        message = ctx.message.content
        if Chatter.is_mod or ctx.author == 'bodedotexe':
            namo = ' '.join(message.split()[1:])
            if namo != '':
                try:
                    if mod.get(namo, 'emylolz') != None:
                        try:
                            while mod.delcmd(namo, 'emylolz') != None:
                                await ctx.channel.send(f'/me {ctx.author.name} -> Emilia lol divorciou-se de {namo}.')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.channel.send(f'/me {ctx.author.name} -> Namorada não encontradokkkk')


@bot.command(name='namorados', aliases=['namoradas','namos'])
async def namorados(ctx):
    if ctx.channel.name == 'marinaetc':
        cmds = list(mod.get("@all", 'marinaetc').values())
        list1 = ''
        listall = []
        a = 1
        for i in cmds:
            if len(list1)+len(i) < 455:
                list1 = list1 + f'{a}º {i}, '
            else:
                listall.append(list1)
                list1 = f'{a}º {i}, '
            a += 1
        if len(listall) > 0:
            for i in range(len(listall)):
                await ctx.channel.send(f'/me Namorados da Etc (Pág. {i+1}): {listall[i]}')
        await ctx.channel.send(f'/me Namorados da Etc (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')
    elif ctx.channel.name == 'emylolz':
        cmds = list(mod.get("@all", 'emylolz').values())
        list1 = ''
        listall = []
        a = 1
        for i in cmds:
            if len(list1)+len(i) < 455:
                list1 = list1 + f'{a}ª {i}, '
            else:
                listall.append(list1)
                list1 = f'{a}ª {i}, '
            a += 1
        if len(listall) > 0:
            for i in range(len(listall)):
                await ctx.channel.send(f'/me Namoradas da Emy (Pág. {i+1}): {listall[i]}')
        await ctx.channel.send(f'/me Namoradas da Emy (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')


@bot.command(name='entrar')
async def join(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        AUTHOR = ctx.message.content.split()[1]
        if ctx.channel.name == BOT_NICK:
            CHANNELS = mod.get_channel()
            if AUTHOR in CHANNELS:
                await ctx.send(f'/me bode JÁ ESTÁ no canal {AUTHOR}')
            else:
                CHANNELS.append(AUTHOR)
                mod.update_channel(CHANNELS)
                await bot.join_channels(CHANNELS)
                await ctx.send(f'/me bode ENTROU no canal {AUTHOR}')


@bot.command(name='sair')
async def leave(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        AUTHOR = ctx.message.content.split()[1]
        if ctx.channel.name == BOT_NICK:
            CHANNELS = mod.get_channel()
            if AUTHOR in CHANNELS:
                CHANNELS.remove(AUTHOR)
                mod.update_channel(CHANNELS)
                await bot.part_channels([AUTHOR])
                await ctx.send(f'/me bode SAIU do canal {AUTHOR}')
            else:
                await ctx.send(f'/me bode NÃO ESTÁ no canal {AUTHOR}')


@bot.command(name='doxadd')
async def doxadd(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        DOXER = ctx.message.content.split()[1]
        DOXERS = mod.get_doxer()
        if ctx.channel.name == BOT_NICK:
            if DOXER in DOXERS:
                await ctx.send(f'/me {DOXER} já se encontra na lista')
            else:
                DOXERS.append(DOXER)
                mod.update_doxer(DOXERS)
                await ctx.send(f'/me {DOXER} adicionado à lista')


@bot.command(name='doxdel')
async def doxdel(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        DOXER = ctx.message.content.split()[1]
        DOXERS = mod.get_doxer()
        if ctx.channel.name == BOT_NICK:
            if DOXER in DOXERS:
                DOXERS.remove(DOXER)
                mod.update_doxer(DOXERS)
                await ctx.send(f'/me {DOXER} removido da lista')
            else:
                await ctx.send(f'/me {DOXER} não está na lista')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('/me pong booudeHMM')


@bot.command(name='amor')
async def ban(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        ban = mod.get_doxer()
        for i in ban:
            await ctx.ban(f'{i} Contas Ip Logger - Em hipótese alguma acesse estes canais')

if __name__ == "__main__":
    bot.run()
