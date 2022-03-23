import os
import re
import static.python.mod as mod
import time
import tweepy
import threading
import asyncio

from random import choice, randint, choices
from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client
from twitchio import PartialUser

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
CHANNELS = mod.get_channel()
BOT_NICK = os.environ.get('BOT_NICK')
TWITTER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

client = Client(
    token=TOKEN,
    heartbeat=30.0
)

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(TWITTER_TOKEN, TWITTER_TOKEN_SECRET)
tweetapi = tweepy.API(auth)
msglist = []
resposta = ['t', '☝️ o de cima é gay', 'quem eh bode choke7Hum', '?', 'choke7Hum marca n dog', '🚬', 'quem me marcou é gay', 'cu',
            'B)', ':7', 'é a porra do bode B)', '👀 ', 'monkaEyes', 'oi', 'para de me marcar', 'to baianor 💤 ', 'não é bode é dani', 'choke7Eai', 'qual a pira? choke7Hum', 'sou eu msm, não é o bot']
voz = ['voz', 'msg', 'tts', 'modvoz', 'msgmod', 'vozmod',
       'modmsg', 'mm', 'msgsub', 'vozsub', 'ms', 'subvoz', 'submsg']


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            prefix=PREFIX,
            token=TOKEN,
            initial_channels=CHANNELS,
            heartbeat=30.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')

    async def event_message(self, message):

        def callback(self, func):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(func)
            loop.close()

        if message.echo:
            return

        autor = message.author.name
        canal = message.channel.name
        content = message.content
        hora = message.timestamp.strftime('%H:%M:%S')
        print(f'#{canal} {hora} {autor}: {content}')

        # Eventos de mensagem para rodar apenas no canal twitch.tv/Choke7
        if canal == 'choke7' and autor != 'streamelements':
            # Respostas automáticas pro chat
            if autor != 'streamelements' and re.search("bode|🐐", content.lower()) is not None:
                a = choice(resposta)
                if a == 't':
                    await message.channel.send(f'choke7Gun {autor}')
                else:
                    await message.channel.send(a)

            # Tweets automáticos
            if message.author.is_subscriber and 10 < len(content) < 217 and len(content.split()) > 2:
                if content[0] == PREFIX and content.split(' ')[0][1:].lower() in voz:
                    msglist.append({"autor": autor, "msg": content})
                elif content[0] != PREFIX:
                    msglist.append({"autor": autor, "msg": content})

                async def autotweet(self):
                    if len(msglist) > 300:
                        a = choice(msglist)
                        msglist.clear()
                        time.sleep(900)
                        content = f'{a["msg"]} (Aleatório de {a["autor"]}) #Choke7'
                        tweetapi.update_status(status=content)
                        id = tweetapi.user_timeline(count=1)[0]
                        await message.channel.send(f'/me Tweet aleatório de @{a["autor"]} pode ser visto em: twitter.com/choke7chat/status/{id.id}')

                threading.Thread(target=callback, args=(
                    self, autotweet(self),)).start()

        # Eventos de mensagem para rodar apenas no canal twitch.tv/Emerok1
        if canal == 'emerok1':
            # Respostas automáticas pro chat
            if autor != 'streamelements' and re.search("bode", content.lower()) is not None:
                await message.channel.send("dani* booudeYUNA")

            # Sorteios para primeiro mês de inscrição
            if autor == 'OFFstreamelements' and re.search("se quiser entrar no grupo do WhatsApp, basta digitar !grupo e o bot manda o link no seu privado", content) is not None:
                # Escolher qualquer skin do jogo 1%
                # Passe Wild 2%
                # x1 contra Emerok 5%
                # Escolher tema do video 5%
                # Adicionar o Emerok 10%
                # Escolher pick 10%
                # Não ganhar nada 27%
                # Ganhar 3000 pontos 40%
                content = content.split(' ', 1)[0]
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
                        key: content[:-1]
                    },
                    "prize": {
                        key: resultado[0]
                    },
                    "date": {
                        key: time.strftime("%d-%m-%Y")
                    }
                }
                mod.addprize(input, 'emerok1')

                async def sorteio(self):
                    time.sleep(15)
                    await message.channel.send(f'/me {content} você ganhou....... {prizes[resultado[0]]}')
                    if resultado[0] == getPrizes[7]:
                        await message.channel.send(f'!addpoints {content[:-1]} 3000')

                threading.Thread(target=callback, args=(
                    self, sorteio(self),)).start()

        await self.handle_commands(message)

    @commands.command(name='tweet')
    @mod.cooldown
    async def tweet(self, ctx: commands.Context, *args):

        # twitch.tv/choke7
        if ctx.channel.name == 'choke7':
            if ctx.author.is_subscriber == True:
                AUTHOR = ctx.author.name
                message = ' '.join(ctx.message.content.split()[1:])
                message = f'{message} (Realizado por {AUTHOR}) #Choke7'
                try:
                    tweetapi.update_status(status=message)
                    id = tweetapi.user_timeline(count=1)[0]
                    await ctx.reply(f'/me Tweet de {AUTHOR} pode ser visto em: twitter.com/choke7chat/status/{id.id}')
                #    await ctx.reply(f'/me Bot offline pra moderação dormir.')
                except:
                    await ctx.reply(f'/me {AUTHOR}, o tweet precisa ser um pouco mais curto.')
            else:
                await ctx.reply(f'/me Tweet disponível apenas para subs.')

    @commands.command(name='testa')
    async def testa(self, ctx: commands.Context):

        # twitch.tv/choke7
        if ctx.channel.name == 'choke7':
            if ctx.author.name == 'choke7':
                await ctx.reply('/me Paula, tua testa é incalculável.')
            elif ctx.author.name == '1bode':
                await ctx.reply('/me testa o q dog? choke7Hum')
            else:
                await ctx.reply(f'/me você tem {randint(7, 30)}cm de testa PIGGERS')

    @commands.command(name='ad', aliases=['pdl', 'pdl1', 'pdl2', 'pdl3'])
    async def commercial_command(self, ctx: commands.Context):

        # precisa de editor no canal
        if ctx.author.is_mod:
            await PartialUser.start_commercial(self, token=TOKEN, length=60)

    @commands.command(name='marker', aliases=['marcar', 'marca', 'm', 'aqui', 'tk'])
    async def create_mark(self, ctx: commands.Context):

        # precisa de editor no canal
        if ctx.author.is_mod:
            _1 = ' '.join(ctx.message.content.split()[1:])
            await ctx.send(f'/marker {_1}')

    @commands.command(name='bode')
    async def bode(self, ctx: commands.Context):

        # twitch.tv/xumartins1
        if ctx.channel.name == 'xumartins1':
            await ctx.send('👀')

    @commands.command(name='gigante', aliases=['giga'])
    async def gigante(self, ctx: commands.Context):

        # twitch.tv/noobzinha
        if ctx.channel.name == 'noobzinha' and ctx.author.is_subscriber:
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
                await ctx.reply(f'/me {namo} adicionado(a) à lista dos gigantescos nbzaAYAYA')
                return
            else:
                await ctx.reply(f'/me Adicione o nome da pessoa ou do objeto colossal após o comando nbzaPalhacinha')

    @commands.command(name='anão', aliases=['anao'])
    async def anao(self, ctx: commands.Context):

        # twitch.tv/noobzinha
        if ctx.channel.name == 'noobzinha' and ctx.author.is_mod:
            message = ctx.message.content
            namo = ' '.join(message.split()[1:])
            if namo != '':
                try:
                    if mod.get_namo(namo, 'noobzinha') != None:
                        try:
                            while mod.delcmd(namo, 'noobzinha') != None:
                                await ctx.reply(f'/me Groselha APARENTEMENTE é maior que {namo} nbzaLUL')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.reply(f'/me Gigantesco descomunal não encontradokkkk nbzaBuxin')

    @commands.command(name='gigantes', aliases=['gigas'])
    @mod.cooldown
    async def gigantes(self, ctx: commands.Context):

        # twitch.tv/noobzinha
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

    @commands.command(name='namorado', aliases=['namorada', 'namo'])
    async def namorado(self, ctx: commands.Context):
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])

        # twitch.tv/marinaetc
        if ctx.channel.name == 'marinaetc':
            if namo != '':
                try:
                    value = int(
                        list(mod.get_namo("@all", 'marinaetc').keys())[-1])+1
                except IndexError:
                    value = 1
                input = {value: namo}
                mod.add(input, 'marinaetc')
                await ctx.reply(f'/me {namo} adicionado à lista de namorados da marinaetc.')
                return
            else:
                await ctx.reply(f'/me Adicione o nome do namorado após o comando')

        # twitch.tv/emylolz
        elif ctx.channel.name == 'emylolz':
            if namo != '':
                try:
                    value = int(
                        list(mod.get_namo("@all", 'emylolz').keys())[-1])+1
                except IndexError:
                    value = 1
                input = {value: namo}
                mod.add(input, 'emylolz')
                await ctx.reply(f'/me {namo} adicionada à lista de namoradas da emy.')
                return
            else:
                await ctx.reply(f'/me Adicione o nome da namorada após o comando')

        # twitch.tv/kiiaraw
        elif ctx.channel.name == 'kiiaraww':
            if namo != '':
                try:
                    value = int(
                        list(mod.get_namo("@all", 'kiiaraww').keys())[-1])+1
                except IndexError:
                    value = 1
                input = {value: namo}
                mod.add(input, 'kiiaraww')
                await ctx.reply(f'/me {namo} adicionada à lista de namoradas da kiara.')
                return
            else:
                await ctx.reply(f'/me Adicione o nome da namorada após o comando')

    @commands.command(name='divorcio')
    async def divorcio(self, ctx: commands.Context):
        message = ctx.message.content
        namo = ' '.join(message.split()[1:])

        # twitch.tv/marinaetc
        if ctx.channel.name == 'marinaetc' and ctx.author.is_mod:
            if namo != '':
                try:
                    if mod.get_namo(namo, 'marinaetc') != None:
                        try:
                            while mod.delcmd(namo, 'marinaetc') != None:
                                await ctx.reply(f'/me Marina Reticências divorciou-se de {namo}.')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.reply(f'/me Namorado não encontradokkkk')

        # twitch.tv/emylolz
        elif ctx.channel.name == 'emylolz' and ctx.author.is_mod:
            if namo != '':
                try:
                    if mod.get_namo(namo, 'emylolz') != None:
                        try:
                            while mod.delcmd(namo, 'emylolz') != None:
                                await ctx.reply(f'/me Emilia lol divorciou-se de {namo}.')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.reply(f'/me Namorada não encontradokkkk')

        # twitch.tv/kiiaraww
        elif ctx.channel.name == 'kiiaraww' and ctx.author.is_mod:
            if namo != '':
                try:
                    if mod.get_namo(namo, 'kiiaraww') != None:
                        try:
                            while mod.delcmd(namo, 'kiiaraww') != None:
                                await ctx.reply(f'/me malasia divorciou-se de {namo}.')
                        except ValueError:
                            return
                except ValueError:
                    await ctx.reply(f'/me Namorada não encontradokkkk')

    @commands.command(name='namorados', aliases=['namoradas', 'namos'])
    async def namorados(self, ctx: commands.Context):

        # twitch.tv/marinaetc
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

        # twitch.tv/emylolz
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

        # twitch.tv/kiiaraww
        elif ctx.channel.name == 'kiiaraww':
            cmds = list(mod.get_namo("@all", 'kiiaraww').values())
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
                    await ctx.channel.send(f'/me Namoradas da Mawasa (Pág. {i+1}): {listall[i]}')
            await ctx.channel.send(f'/me Namoradas da Mawasa (Pág. {len(listall)+1}): {list1} Total: {len(cmds)}')

    @commands.command(name='entrar')
    async def join(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
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

    @commands.command(name='sair')
    async def leave(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
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

    @commands.command(name='doxadd')
    async def doxadd(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
            DOXER = ctx.message.content.split()[1]
            DOXERS = mod.get_doxer()
            if ctx.channel.name == BOT_NICK:
                if DOXER in DOXERS:
                    await ctx.send(f'/me {DOXER} já se encontra na lista')
                else:
                    DOXERS.append(DOXER)
                    mod.update_doxer(DOXERS)
                    await ctx.send(f'/me {DOXER} adicionado à lista')

    @commands.command(name='doxdel')
    async def doxdel(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
            DOXER = ctx.message.content.split()[1]
            DOXERS = mod.get_doxer()
            if ctx.channel.name == BOT_NICK:
                if DOXER in DOXERS:
                    DOXERS.remove(DOXER)
                    mod.update_doxer(DOXERS)
                    await ctx.send(f'/me {DOXER} removido da lista')
                else:
                    await ctx.send(f'/me {DOXER} não está na lista')

    @commands.command(name='doxban')
    async def ban(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
            ban = mod.get_doxer()
            for i in ban:
                await ctx.ban(f'{i} Contas Ip Logger - Em hipótese alguma acesse estes canais')

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        await ctx.reply('/me pong booudeHMM')


bot = Bot()

# comando para git pull pelo chat
# @commands.command(name="update")
# async def update(self, ctx: commands.Context):
#     if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
#         os.system("git pull")
#         print("Atualizando e reiniciando...")
#         os.system("python3 bot.py")
#         exit()
