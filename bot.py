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
async def event_message(ctx):
    marinaetc = ['marina43Etcetera', 'marina43Love',
                 'marina43Oclinhos', 'marina43Reza', 'marina43Trail', 'marina43Testalol', 'marina43Gatilh']
    CHANNEL = ctx.channel.name
    message = ctx.content
    content = message.split()
    if CHANNEL == 'marinaetc':
        if ctx.author.name != BOT_NICK:
            if set(content) & set(marinaetc):
                await ctx.channel.send(f'{choice(marinaetc)}')
        if message[0] == PREFIX:
            cmds = message.split(' ')[0][1:].lower()
            if cmds == 'namorado':
                message = message.replace(
                    f'{PREFIX}{cmds}', '').strip()
                opt = message.split()[0]
                if opt != '':
                    try:
                        value = int(
                            list(mod.get("@all", CHANNEL).keys())[-1])+1
                    except IndexError:
                        value = 1
                    input = {value: opt}
                    mod.add(input, CHANNEL)
                    await ctx.channel.send(f'{ctx.author.name} -> {opt} adicionado à lista de namorados da marinaetc.')
                    return
                else:
                    await ctx.channel.send(f'{ctx.author.name} -> Adicione o nome do namorado após o comando')
            elif cmds == 'divorcio':
                if Chatter.is_mod or ctx.author == 'bodedotexe':
                    message = message.replace(
                        f'{PREFIX}{cmds}', '').strip()
                    opt = message.split()[0]
                    if opt != '':
                        try:
                            if mod.get(opt, CHANNEL) != None:
                                try:
                                    while mod.delcmd(opt, CHANNEL) != None:
                                        await ctx.channel.send(f'{ctx.author.name} -> Marina Reticências divorciou-se de {opt}.')
                                except ValueError:
                                    return
                        except ValueError:
                            await ctx.channel.send(f'{ctx.author.name} -> Namorado não encontradokkkk')
    if CHANNEL == 'emylolz':
        if message[0] == PREFIX:
            cmds = message.split(' ')[0][1:].lower()
            if cmds == 'namorada':
                message = message.replace(
                    f'{PREFIX}{cmds}', '').strip()
                opt = message.split()[0]
                if opt != '':
                    try:
                        value = int(
                            list(mod.get("@all", CHANNEL).keys())[-1])+1
                    except IndexError:
                        value = 1
                    input = {value: opt}
                    mod.add(input, CHANNEL)
                    await ctx.channel.send(f'{ctx.author.name} -> {opt} adicionado à lista de namoradas da emy.')
                    return
                else:
                    await ctx.channel.send(f'{ctx.author.name} -> Adicione o nome da namorada após o comando')
            elif cmds == 'divorcio':
                if Chatter.is_mod or ctx.author == 'bodedotexe':
                    message = message.replace(
                        f'{PREFIX}{cmds}', '').strip()
                    opt = message.split()[0]
                    if opt != '':
                        try:
                            if mod.get(opt, CHANNEL) != None:
                                try:
                                    while mod.delcmd(opt, CHANNEL) != None:
                                        await ctx.channel.send(f'{ctx.author.name} -> Emilia LoL divorciou-se de {opt}.')
                                except ValueError:
                                    return
                        except ValueError:
                            await ctx.channel.send(f'{ctx.author.name} -> Namorado não encontradokkkk')
    await bot.handle_commands(ctx)


@bot.command(name='bode')
async def command_bode(ctx):
    if ctx.channel.name == 'xumartins1':
        await ctx.channel.send('👀')


@bot.command(name='namorados')
async def command_namos(ctx):
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
                await ctx.channel.send(f'Namorados da Etc (Pág. {i+1}): {listall[i]}')
        await ctx.channel.send(f'Namorados da Etc (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')


@bot.command(name='namoradas')
async def command_namos(ctx):
    if ctx.channel.name == 'emylolz':
        cmds = list(mod.get("@all", 'emylolz').values())
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
                await ctx.channel.send(f'Namoradas da Emy (Pág. {i+1}): {listall[i]}')
        await ctx.channel.send(f'Namoradas da Emy (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')


@bot.command(name='entrar')
async def command_join(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        AUTHOR = ctx.message.content.split()[1]
        if ctx.channel.name == BOT_NICK:
            CHANNELS = mod.get_channel()
            if AUTHOR in CHANNELS:
                await ctx.send(f'bode JÁ ESTÁ no canal {AUTHOR}')
            else:
                CHANNELS.append(AUTHOR)
                mod.update_channel(CHANNELS)
                await bot.join_channels(CHANNELS)
                await ctx.send(f'bode ENTROU no canal {AUTHOR}')


@bot.command(name='sair')
async def command_leave(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        AUTHOR = ctx.message.content.split()[1]
        if ctx.channel.name == BOT_NICK:
            CHANNELS = mod.get_channel()
            if AUTHOR in CHANNELS:
                CHANNELS.remove(AUTHOR)
                mod.update_channel(CHANNELS)
                await bot.part_channels([AUTHOR])
                await ctx.send(f'bode SAIU do canal {AUTHOR}')
            else:
                await ctx.send(f'bode NÃO ESTÁ no canal {AUTHOR}')


@bot.command(name='doxadd')
async def command_join(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        DOXER = ctx.message.content.split()[1]
        DOXERS = mod.get_doxer()
        if ctx.channel.name == BOT_NICK:
            if DOXER in DOXERS:
                await ctx.send(f'{DOXER} já se encontra na lista')
            else:
                DOXERS.append(DOXER)
                mod.update_doxer(DOXERS)
                await ctx.send(f'{DOXER} adicionado à lista')


@bot.command(name='doxdel')
async def command_leave(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        DOXER = ctx.message.content.split()[1]
        DOXERS = mod.get_doxer()
        if ctx.channel.name == BOT_NICK:
            if DOXER in DOXERS:
                DOXERS.remove(DOXER)
                mod.update_doxer(DOXERS)
                await ctx.send(f'{DOXER} removido da lista')
            else:
                await ctx.send(f'{DOXER} não está na lista')


@bot.command(name='ping')
async def command_ping(ctx):
    await ctx.send('pong booudeHMM')


@bot.command(name='amor')
async def command_ban(ctx):
    AUTHOR = ctx.author.name
    if AUTHOR == '1bode':
        ban = mod.get_doxer()
        for i in ban:
            await ctx.ban(f'{i} Contas Ip Logger - Em hipótese alguma acesse estes canais')

if __name__ == "__main__":
    bot.run()
