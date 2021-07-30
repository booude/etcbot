import os
import mod

from random import choice
from dotenv import load_dotenv
from os.path import join
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
CHANNELS = mod.get_channel()

bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNELS
)

client = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)


@bot.event
async def event_ready():
    print(f"{BOT_NICK} ta online!")

newcmd = ''


@bot.event
async def event_message(ctx):
    marinaetc = ['marina43Etcetera', 'marina43Love',
                 'marina43Oclinhos', 'marina43Reza', 'marina43Trail', 'marina43Testalol']
    ninaetc = ['marina', 'nina', 'marinaetc']
    if ctx.author.name.lower() == BOT_NICK.lower():
        return
    global CHANNEL
    CHANNEL = ctx.channel.name.lower()
    message = ctx.content
    content = message.split()
    marina = 0
    for i in content:
        if i in marinaetc:
            marina += 1
    if marina != 0:
        await ctx.channel.send(f'{choice(marinaetc)}')
    nina = 0
    for i in content:
        if i in ninaetc:
            nina += 1
    if nina != 0:
        return
#        await ctx.channel.send('marina? voce quis dizer minha webnamorada?')
    if message[0] == BOT_PREFIX:
        cmds = message.split(' ')[0][1:].lower()
        if cmds == 'namorado':
            if ctx.author != '':
                message = message.replace(f'{BOT_PREFIX}{cmds}', '').strip()
                opt = message.split()[0]
                if opt != '':
                    try:
                        value = int(
                            list(mod.get("@all", CHANNEL).keys())[-1])+1
                    except IndexError:
                        value = 1
                    input = {value: opt}
                    mod.add(input, CHANNEL)
                    await ctx.channel.send_me(f'{ctx.author.name} -> {opt} adicionado à lista de namorados da marinaetc.')
                    return
                else:
                    await ctx.channel.send_me(f'{ctx.author.name} -> Adicione o nome do namorado após o comando')
        elif cmds == 'divorcio':
            if ctx.author.is_mod or ctx.author == CHANNEL:
                message = message.replace(f'{BOT_PREFIX}{cmds}', '').strip()
                opt = message.split()[0]
                if opt != '':
                    try:
                        if mod.get(opt, CHANNEL) != None:
                            try:
                                while mod.delcmd(opt, CHANNEL) != None:
                                    await ctx.channel.send_me(f'{ctx.author.name} -> Marina Reticências divorciou-se de {opt}.')
                            except ValueError:
                                return
                    except ValueError:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Namorado não encontradokkkk')
    await bot.handle_commands(ctx)


@bot.command(name='namorados')
async def command_namos(ctx):
    cmds = list(mod.get("@all", CHANNEL).values())
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
            await ctx.channel.send_me(f'Namorados da Etc (Pág. {i+1}): {listall[i]}')
    await ctx.channel.send_me(f'Namorados da Etc (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')

# @bot.command(name='elo')
# async def command_elo(ctx):
#    await ctx.send('KKKKKKKKKKKKKKKKKKKKKKKKKKKKK EXCLAMAÇÃO ELO')

# @bot.command(name='tinder')
# async def command_tinder(ctx):
#    await ctx.send('1bode deu match com marinaetc. o amor é lindo marina43Love')

if __name__ == "__main__":
    bot.run()
