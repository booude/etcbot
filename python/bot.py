import os
import re
import mod
import time
import tweepy
import threading
import asyncio

from random import choice, randint, choices
from dotenv import load_dotenv
from os.path import join
from twitchio import Chatter, PartialUser
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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
msglist = []


@bot.event()
async def event_ready():
    print("ta on crl")


@bot.event()
async def event_message(message):
    resposta = ['t', '☝️ o de cima é gay', 'quem eh bode choke7Hum', '?', 'choke7Hum marca n dog', '🚬', 'quem me marcou é gay', 'cu',
                'B)', ':7', 'é a porra do bode B)', '👀 ', 'monkaEyes', 'oi', 'para de me marcar', 'to baianor 💤 ', 'não é bode é dani', 'choke7Eai', 'qual a pira? choke7Hum', 'sou eu msm, não é o bot']
    if message.echo:
        return
    autor = message.author.name
    CHANNEL = message.channel.name
    msg = message.content
    hora = message.timestamp.strftime('%H:%M:%S')
    print(f'#{CHANNEL} {hora} {autor}: {msg}')
    if CHANNEL == 'choke7':
        if autor != '1bode' and autor != 'streamelements':
            if re.search("bode|🐐", msg.lower()) is not None:
                a = choice(resposta)
                if a == 't':
                    await message.channel.send(f'choke7Gun {autor}')
                else:
                    await message.channel.send(a)
            if 10 < len(msg) < 217:
                if len(msg.split()) > 2:
                    if message.author.is_subscriber:
                        if msg[0] == PREFIX:
                            voz = ['voz', 'msg', 'tts', 'modvoz', 'msgmod', 'vozmod',
                                   'modmsg', 'mm', 'msgsub', 'vozsub', 'ms', 'subvoz', 'submsg']
                            if msg.split(' ')[0][1:].lower() in voz:
                                msglist.append({"autor": autor, "msg": msg})
                        else:
                            msglist.append({"autor": autor, "msg": msg})

            async def delayed():
                if len(msglist) > 300:
                    a = choice(msglist)
                    msglist.clear()
                    time.sleep(900)
                    await autotweet(a)

            async def autotweet(a):
                msg = f'{a["msg"]} (Aleatório de {a["autor"]}) #Choke7'
                tweetapi.update_status(status=msg)
                id = tweetapi.user_timeline(count=1)[0]
                await message.channel.send(f'/me Tweet aleatório de @{a["autor"]} pode ser visto em: twitter.com/choke7chat/status/{id.id}')

            def b_call():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(delayed())
                loop.close()
            t = threading.Thread(target=b_call)
            t.start()
    if CHANNEL == 'emerok1':
        if autor != BOT_NICK and autor != 'streamelements':
            if re.search("bode", msg.lower()) is not None:
                await message.channel.send("dani* booudeYUNA")
        if autor == 'streamelements':
            if re.search("se quiser entrar no grupo do WhatsApp, basta digitar !grupo e o bot manda o link no seu privado", msg) is not None:
                # Escolher qualquer skin do jogo 1%
                # Passe Wild 2%
                # x1 contra Emerok 5%
                # Escolher tema do video 5%
                # Adicionar o Emerok 10%
                # Escolher pick 10%
                # Não ganhar nada 27%
                # Ganhar 3000 pontos 40%
                msg = msg.split(' ', 1)[0]
                getPrizes = [0, 1, 2, 3, 4, 5, 6, 7]
                prizes = ['QUALQUER SKIN DO JOGO!!!', 'UM PASSE WILD!!!', 'X1 CONTRA O PRÓPRIO EMEROKLOL!!!', 'ESCOLHA UM TEMA DE VÍDEO DO YOUTUBE!!!',
                          'ADICIONAR O EMEROK NO WILD RIFT!!!', 'O PODER DE ESCOLHER UM CAMPEÃO!!!', 'NADAKKKKKKK booudeYUNA', '3000 PONTOS NA LOJINHA!!!']
                resultado = []
                resultado = choices(getPrizes, weights=(
                    1, 0, 5, 5, 10, 10, 27, 40))
                try:
                    key = int(list(mod.get_prizes("@all", 'emerok1')
                              ["twitchId"].keys())[-1])+1
                except KeyError:
                    key = 0
                input = {
                    "twitchId": {
                        key: msg[:-1]
                    },
                    "prize": {
                        key: resultado[0]
                    },
                    "date": {
                        key: time.strftime("%d-%m-%Y")
                    }
                }
                mod.addprize(input, 'emerok1')

                async def delayed_():
                    time.sleep(15)
                    await message.channel.send(f'/me {msg} você ganhou....... {prizes[resultado[0]]}')
                    if resultado[0] == getPrizes[7]:
                        await message.channel.send(f'!addpoints {msg[:-1]} 3000')

                def b_call_(args):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(delayed_())
                    loop.close()
                t_ = threading.Thread(target=b_call_, args='a')
                t_.start()


@bot.command(name="tweet")
@mod.cooldown
async def tweet(ctx, *args):
    if ctx.channel.name == 'choke7':
        if ctx.author.is_subscriber == True:
            AUTHOR = ctx.author.name
            message = ' '.join(ctx.message.content.split()[1:])
            message = f'{message} (Realizado por {AUTHOR}) #Choke7'
            try:
                tweetapi.update_status(status=message)
                id = tweetapi.user_timeline(count=1)[0]
                await ctx.channel.send(f'/me Tweet de {AUTHOR} pode ser visto em: twitter.com/choke7chat/status/{id.id}')
            #    await ctx.channel.send(f'/me Bot offline pra moderação dormir.')
            except:
                await ctx.channel.send(f'/me {AUTHOR}, o tweet precisa ser um pouco mais curto.')
        else:
            await ctx.channel.send(f'/me Tweet disponível apenas para subs.')


@bot.command(name='testa')
async def testa(ctx):
    if ctx.channel.name == 'choke7':
        if ctx.author.name == 'choke7':
            await ctx.channel.send('/me Paula, tua testa é incalculável.')
        elif ctx.author.name == '1bode':
            await ctx.channel.send('/me testa o q dog? choke7Hum')
        else:
            await ctx.channel.send(f'/me {ctx.author.name}, você tem {randint(7, 30)}cm de testa PIGGERS')


@bot.command(name='t', aliases=['marcar', 'marca', 'm', 'aqui'])
async def create_marker(ctx):
    if Chatter.is_mod:
        _1 = ' '.join(ctx.message.content.split()[1:])
        await PartialUser.create_marker(token=TOKEN, description=_1)


@bot.command(name='bode')
async def bode(ctx):
    if ctx.channel.name == 'xumartins1':
        await ctx.channel.send('👀')


@bot.command(name='gigante', aliases=['giga'])
async def gigante(ctx):
    if ctx.channel.name == 'noobzinha' and Chatter.is_subscriber:
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])
        if namo != '':
            try:
                value = int(
                    list(mod.get_namo("@all", 'noobzinha').keys())[-1])+1
            except IndexError:
                value = 1
            input = {value: namo}
            mod.add(input, 'noobzinha')
            await ctx.channel.send(f'/me {ctx.author.name} -> {namo} adicionado(a) à lista dos gigantescos nbzaAYAYA')
            return
        else:
            await ctx.channel.send(f'/me {ctx.author.name} -> Adicione o nome da pessoa ou do objeto colossal após o comando nbzaPalhacinha')


@bot.command(name='anão', aliases=['anao'])
async def anao(ctx):
    if ctx.channel.name == 'noobzinha' and Chatter.is_mod:
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])
        if namo != '':
            try:
                if mod.get_namo(namo, 'noobzinha') != None:
                    try:
                        while mod.delcmd(namo, 'noobzinha') != None:
                            await ctx.channel.send(f'/me {ctx.author.name} -> Groselha APARENTEMENTE é maior que {namo} nbzaLul')
                    except ValueError:
                        return
            except ValueError:
                await ctx.channel.send(f'/me {ctx.author.name} -> Gigantesco descomunal não encontradokkkk nbzaBuxin')


@bot.command(name='gigantes', aliases=['gigas'])
async def gigantes(ctx):
    if ctx.channel.name == 'noobzinha':
        cmds = list(mod.get_namo("@all", 'noobzinha').values())
        list1 = ''
        listall = []
        a = 1
        for i in cmds:
            if len(list1)+len(i) < 400:
                list1 = list1 + f'{a}º {i}, '
            else:
                listall.append(list1)
                list1 = f'{a}º {i}, '
            a += 1
        if len(listall) > 0:
            for i in range(len(listall)):
                await ctx.channel.send(f'/me Lista de Pessoas/Coisas maiores que a XL nbzaAnotando (Pág. {i+1}): {listall[i]}')
        await ctx.channel.send(f'/me Lista de Pessoas/Coisas maiores que a XL nbzaAnotando (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')


@bot.command(name='namorado', aliases=['namorada', 'namo'])
async def namorado(ctx):
    if ctx.channel.name == 'marinaetc':
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])
        if namo != '':
            try:
                value = int(
                    list(mod.get_namo("@all", 'marinaetc').keys())[-1])+1
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
                value = int(list(mod.get_namo("@all", 'emylolz').keys())[-1])+1
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
                    if mod.get_namo(namo, 'marinaetc') != None:
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
                    if mod.get_namo(namo, 'emylolz') != None:
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
        cmds = list(mod.get_namo("@all", 'marinaetc').values())
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
        cmds = list(mod.get_namo("@all", 'emylolz').values())
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
    if Chatter.name == BOT_NICK:
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
    if Chatter.name == BOT_NICK:
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
    if Chatter.name == BOT_NICK:
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
    if Chatter.name == BOT_NICK:
        DOXER = ctx.message.content.split()[1]
        DOXERS = mod.get_doxer()
        if ctx.channel.name == BOT_NICK:
            if DOXER in DOXERS:
                DOXERS.remove(DOXER)
                mod.update_doxer(DOXERS)
                await ctx.send(f'/me {DOXER} removido da lista')
            else:
                await ctx.send(f'/me {DOXER} não está na lista')


@bot.command(name='doxban')
async def ban(ctx):
    if Chatter.name == BOT_NICK:
        ban = mod.get_doxer()
        for i in ban:
            await ctx.ban(f'{i} Contas Ip Logger - Em hipótese alguma acesse estes canais')


# comando para git pull pelo chat
# @bot.command(name="update")
# async def update(ctx):
#     if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
#         os.system("git pull")
#         print("Atualizando e reiniciando...")
#         os.system("python3 bot.py")
#         exit()

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('/me pong booudeHMM')


if __name__ == "__main__":
    bot.run()
