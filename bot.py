import os
import re
import mod
import time
import tweepy
import sys

from random import choice, randint
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
BOT_NICK = os.environ.get('BOT_NICK')
TWITTER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

bot = commands.Bot(
    prefix=PREFIX,
    token=TOKEN,
    initial_channels=CHANNELS,
    heartbeat=30.0
)

client = Client(
    token=TOKEN,
    heartbeat=30.0
)

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(TWITTER_TOKEN, TWITTER_TOKEN_SECRET)
tweetapi = tweepy.API(auth)
global _a
_a = True

@bot.event()
async def event_ready():
    print("ta on crl")


@bot.event()
async def event_message(message):
    resposta = ['t', '☝️ o de cima é gay', 'quem eh bode choke7Hum', '?', 'choke7Hum marca n dog', '🚬', 'quem me marcou é gay', 'cu',
                'B)', ':7', 'é a porra do bode B)', '👀 ', 'monkaEyes', 'oi', 'para de me marcar', 'to baianor 💤 ', 'não é bode é dani', 'choke7Eai', 'qual a pira? choke7Hum', 'sou eu msm, não é o bot']
    try:
        autor = message.author.name
    except AttributeError:
        return
    CHANNEL = message.channel.name
    msg = message.content
    time = message.timestamp.strftime('%H:%M:%S')
    print(f'#{CHANNEL} {time} {autor}: {msg}')
    if CHANNEL == 'choke7':
        if autor != '1bode' and autor != 'streamelements':
            if re.search("bode|🐐", msg) is not None:
                a = choice(resposta)
                if a == 't':
                    await message.channel.send(f'choke7Gun {autor}')
                else:
                    await message.channel.send(a)
@bot.command(name="off", aliases=['on'])
async def off(ctx):
    if ctx.author.name == '1bode':
        if _a == False:
            _a == True
    else:
        _a == False

@bot.command(name="tweet")
@mod.cooldown
async def tweet(ctx, *args):
    if ctx.channel.name == 'choke7':
        AUTHOR = ctx.author.name
        message = ' '.join(ctx.message.content.split()[1:])
        message = f'{message} #Choke7 (Realizado por {AUTHOR})'
        try:
            if _a == True:
                tweetapi.update_status(status=message)
                await ctx.channel.send(f'/me Tweet de {AUTHOR} pode ser visto em: twitter.com/choke7chat')
            else:
                await ctx.channel.send(f'/me Bot offline pra moderação dormir.')
        except:
            await ctx.channel.send(f'/me {AUTHOR}, o tweet precisa ser um pouco mais curto.')


@bot.command(name="update")
async def update(ctx):
    if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
        os.system("git pull")
        print("Atualizando e reiniciando...")
        os.system("python3 bot.py")
        exit()


@bot.command(name='testa')
async def testa(ctx):
    if ctx.channel.name == 'choke7':
        if ctx.author.name == 'choke7':
            await ctx.channel.send('/me Paula, tua testa é incalculável.')
        elif ctx.author.name == '1bode':
            await ctx.channel.send('/me testa o q dog? choke7Hum')
        else:
            await ctx.channel.send(f'/me {ctx.author.name}, você tem {randint(7, 30)}cm de testa PIGGERS')


@bot.command(name='bode')
async def bode(ctx):
    if ctx.channel.name == 'xumartins1':
        await ctx.channel.send('👀')


@bot.command(name='namorado', aliases=['namorada', 'namo'])
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


@bot.command(name='namorados', aliases=['namoradas', 'namos'])
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
