import os
import re
import static.python.db_modules as mod
import tweepy
import requests

from static.python.utils import json, threading
from random import choice, randint, choices
from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_NICK = os.environ.get('BOT_NICK')

TWITTER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

msglist = []
prediction = ''
win = ''
lose = ''

client = Client(
    token=TOKEN,
    client_secret=CLIENT_SECRET,
    heartbeat=20.0
)

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(TWITTER_TOKEN, TWITTER_TOKEN_SECRET)
tweetapi = tweepy.API(auth)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            prefix=PREFIX,
            token=TOKEN,
            client_secret=CLIENT_SECRET,
            initial_channels=[BOT_NICK],
            heartbeat=20.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')
        await bot.join_channels(await mod.get_channels())

    async def event_message(self, message):

        if message.echo:
            return

        autor = message.author.name
        canal = message.channel.name
        content = message.content
        hora = message.timestamp.strftime('%H:%M:%S')
        print(f'#{canal} {hora} {autor}: {content}')

        # Skip bot messages
        if autor != BOT_NICK:
            # Eventos de mensagem para rodar apenas no canal twitch.tv/Choke7
            if canal == 'choke7' and autor != 'streamelements':
                utils = json.loadutils(canal)
                # Respostas automáticas pro chat
                if autor != 'streamelements' and re.search(utils['searchAnswer'], content.lower()) is not None:
                    answer = choice(utils['resposta'])
                    if answer == 'timeout':
                        await message.channel.send(f'choke7Gun {autor}')
                    else:
                        await message.channel.send(answer)
                # if (autor == 'veazy' or autor == 'aquelafoca_o_peverso') and content.split(' ')[0] == '/me':
                #     await message.channel.send(f'choke7Gun {autor}')

                # Tweets automáticos
                if message.author.is_subscriber and 10 < len(content) < 217 and len(content.split()) > 2:
                    if content[0] == PREFIX and content.split(' ')[0][1:].lower() in utils['voz']:
                        msglist.append({"autor": autor, "msg": content})
                    elif content[0] != PREFIX:
                        msglist.append({"autor": autor, "msg": content})
                    _t = threading.thread_create
                    _t(self, threading.autotweet, message, msglist, tweetapi)

            # Eventos de mensagem para rodar apenas no canal twitch.tv/Emerok1
            if canal == 'off':
                utils = json.loadutils(canal)
                # Respostas automáticas pro chat
                if autor != 'streamelements' and re.search(utils['searchAnswer'], content.lower()) is not None and re.search('@1bode', content.lower()) is None:
                    answer = choice(utils['resposta'])
                    await message.channel.send(answer)

            if canal == 'noobzinha':
                # Contador de perda de fios de cabelo
                json.count(autor, canal)

        await self.handle_commands(message)

    @commands.command(name='nick')
    @commands.cooldown(1, 5)
    async def nick(self, ctx: commands.Context):
        if ctx.channel.name == 'tetiszin':
            await ctx.send('/me meu nick eh tetis pq na vdd eu amo jogar tetris é meu main jogo kkkkkkserio passo mais tempo jogando tetris do que o proprio lol enfim só ver a gameplay ne.. dai eu escrevi tetis mesmo pq achava q chamava tetis 😂 😂 ai ai como sou burrinho depois descobri q tinha um R daí n deu mais como mudar')

    @commands.command(name='apresentação', aliases=['apresentacao', 'apresentaçao', 'apresentacão'])
    @commands.cooldown(1, 5)
    async def apresentacao(self, ctx: commands.Context):
        if ctx.channel.name == 'tetiszin':
            await ctx.send('/me boa noite meu nome é tetris tenho 36 anos, jogo wild rift 16 horas por dia e ainda não consegui passar do elo do emerok (streamer cansadokk). se alguem quiser saber onde fiz o implante foi na indonésia, reimplantado do couro escrotal msm rs. sou main jg..... testei as outras rotas e n saí do esmeralda (ainda bem q a tsm me contratou sem saber desse detalhe). então é isso rapaziada sejam bem vindos live todos os dias das 7h as 21h fé no pai 🙏')

    @commands.command(name='unha')
    @commands.cooldown(1, 5)
    async def unha(self, ctx: commands.Context):
        if ctx.channel.name == 'tetiszin':
            await ctx.send('/me tetris....... eu sei que é melhor limpar com a mão...... mas depois a gente lava com sabão pra tirar a sobra q fica por debaixo da unha kk')

    @commands.command(name='celular', aliases=['cel', 'phone', 'cell'])
    @commands.cooldown(1, 5)
    async def celular(self, ctx: commands.Context):
        if ctx.channel.name == 'tetiszin':
            await ctx.send('/me samsung galaxy pocket gt s5310b tela levemente trincada no canto inferior esquerdo bateria viciada')

    @commands.command(name='tweet')
    @commands.cooldown(1, 15)
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
                    await ctx.reply(f'Tweet de {AUTHOR} pode ser visto em: twitter.com/choke7chat/status/{id.id}')
                #    await ctx.reply(f'/me Bot offline pra moderação dormir.')
                except:
                    await ctx.reply(f'O tweet precisa ser um pouco mais curto.')
            else:
                await ctx.reply(f'Tweet disponível apenas para subs.')

    @commands.command(name='testa')
    @commands.cooldown(1, 1)
    async def testa(self, ctx: commands.Context):

        # twitch.tv/choke7
        if ctx.channel.name == 'choke7':
            if ctx.author.name == 'choke7':
                await ctx.reply('Paula, tua testa é incalculável.')
            elif ctx.author.name == BOT_NICK:
                await ctx.reply('Testa o q dog? choke7Hum')
            else:
                await ctx.reply(f'Você tem {randint(7, 30)}cm de testa PIGGERS')

    @commands.command(name='ad', aliases=['win', 'lose'])
    @commands.cooldown(1, 1)
    async def commercial_command(self, ctx: commands.Context):
        if ctx.channel.name == 'emerok1' and ctx.author.is_mod:
            message = ctx.message.content
            emerok_token = requests.post('https://id.twitch.tv/oauth2/token', data={
                "client_id": f"{CLIENT_ID}", "client_secret": f"{CLIENT_SECRET}", "grant_type": "refresh_token", "refresh_token": f"{REFRESH_TOKEN}"}).json()["access_token"]
            length = 180
            res = requests.post(f'https://api.twitch.tv/helix/channels/commercial?broadcaster_id=59252262&length={length}', headers={
                "Authorization": f"Bearer {emerok_token}", "Client-Id": f"{CLIENT_ID}", "ContentType": "application/json"})
            try:
                if res.json()["data"]:
                    await ctx.send('/me Passando um AD rapaziada emerokAYAYA !mercerok')
            except:
                print(res.json()["status"], res.json()["message"])
            try:
                if message.split()[0] == '!win':
                    parameters = {
                        "broadcaster_id": "59252262",
                        "id": prediction,
                        "status": "RESOLVED",
                        "winning_outcome_id": win
                    }
                    requests.patch(f'https://api.twitch.tv/helix/predictions', headers={
                        "Authorization": f"Bearer {emerok_token}", "Client-Id": f"{CLIENT_ID}", "ContentType": "application/json"}, json=parameters)
                    await ctx.send('/me APOSTINHAS FORAM PAGAS!!! O AZUL VENCEU!!! emerokAYAYA emerokAYAYA emerokAYAYA')

                elif message.split()[0] == '!lose':
                    parameters = {
                        "broadcaster_id": "59252262",
                        "id": prediction,
                        "status": "RESOLVED",
                        "winning_outcome_id": lose
                    }
                    requests.patch(f'https://api.twitch.tv/helix/predictions', headers={
                        "Authorization": f"Bearer {emerok_token}", "Client-Id": f"{CLIENT_ID}", "ContentType": "application/json"}, json=parameters)
                    await ctx.send('/me APOSTINHAS FORAM PAGAS!!! O ROSA VENCEU!!! emerokAYAYA emerokAYAYA emerokAYAYA')
            except:
                pass

    @commands.command(name='marker', aliases=['marcar', 'marca', 'm', 'aqui', 'tk'])
    @commands.cooldown(1, 1)
    async def create_mark(self, ctx: commands.Context):
        if ctx.channel.name == 'emerok1' and ctx.author.is_mod:
            emerok_token = requests.post('https://id.twitch.tv/oauth2/token', data={
                "client_id": f"{CLIENT_ID}", "client_secret": f"{CLIENT_SECRET}", "grant_type": "refresh_token", "refresh_token": f"{REFRESH_TOKEN}"}).json()["access_token"]
            try:
                description = ' '.join(ctx.message.content.split()[1:])
            except:
                description = ''
            res = requests.post(f'https://api.twitch.tv/helix/streams/markers?user_id=59252262&description={description}', headers={
                "Authorization": f"Bearer {emerok_token}", "Client-Id": f"{CLIENT_ID}", "ContentType": "application/json"})
            try:
                if res.json()["data"]:
                    await ctx.reply(f'Marcação criada no VOD com a descrição: {description} emerokNoted')
            except:
                print(res.json()["status"], res.json()["message"])

    @commands.command(name='apostinha', aliases=['prediction', 'palpite', 'palpites', 'apostinhas', 'predictions'])
    async def prediction(self, ctx: commands.Context):
        if ctx.channel.name == 'emerok1' and ctx. author.is_mod:
            global prediction, win, lose
            emerok_token = requests.post('https://id.twitch.tv/oauth2/token', data={
                "client_id": f"{CLIENT_ID}", "client_secret": f"{CLIENT_SECRET}", "grant_type": "refresh_token", "refresh_token": f"{REFRESH_TOKEN}"}).json()["access_token"]
            outcomes = [{"title": "CLARO SEMPRE"},
                        {"title": "DESSA VEZ NÃO...."}]
            parameters = {"broadcaster_id": "59252262",
                          "title": "EMEROK VAI VENCER? 🤨", "outcomes": outcomes, "prediction_window": 300}
            res = requests.post(f'https://api.twitch.tv/helix/predictions', headers={
                "Authorization": f"Bearer {emerok_token}", "Client-Id": f"{CLIENT_ID}", "ContentType": "application/json"}, json=parameters)
            prediction = res.json()['data'][0]['id']
            win, lose = res.json()['data'][0]['outcomes'][0]['id'], res.json()[
                'data'][0]['outcomes'][1]['id']
            await ctx.send('/me APOSTINHAS ON RAPAZIADA!!! emerokAYAYA emerokAYAYA emerokAYAYA')

    @commands.command(name='bode')
    @commands.cooldown(1, 1)
    async def bode(self, ctx: commands.Context):

        # twitch.tv/xumartins1
        if ctx.channel.name == 'xumartins1':
            await ctx.send('👀')

    @commands.command(name='calvicie')
    @commands.cooldown(1, 3)
    async def calvicie(self, ctx: commands.Context):
        canal = ctx.channel.name
        author = ctx.author.name
        autor = ctx.message.content.split(' ')[1:]
        if canal == 'noobzinha':
            utils = json.loadutils(canal)
            if author != '1bode':
                if autor != []:
                    try:
                        author = autor[0].lower()
                        author = author[1:] if author[0] == '@' else author
                        counter = int(utils[f'{author}']/50)
                    except:
                        counter = int(utils[f'{author}']/50)
                else:
                    counter = int(utils[f'{author}']/50)
                await ctx.send(f'/me {author} já perdeu {counter} fios de cabelo assistindo a essa live nbzaCalva')
            else:
                if autor != []:
                    try:
                        author = autor[0].lower()
                        author = author[1:] if author[0] == '@' else author
                        counter = int(utils[f'{author}']/50)
                        await ctx.send(f'/me {author} já perdeu {counter} fios de cabelo assistindo a essa live nbzaCalva')
                    except:
                        await ctx.send(f'/me {author}, você NUNCA perderá um único fio de cabelo!! nbzaMandrake')
                else:
                    await ctx.send(f'/me {author}, você NUNCA perderá um único fio de cabelo!! nbzaMandrake')

    @commands.command(name='gigante', aliases=['giga'])
    @commands.cooldown(1, 1)
    async def gigante(self, ctx: commands.Context):

        # twitch.tv/noobzinha
        if ctx.channel.name == 'noobzinha' and ctx.author.is_subscriber:
            channel = ctx.channel.name
            author = ctx.author.name
            message = ctx.message.content
            name = ' '.join(message.split()[1:])
            if name != '':
                await mod.add_list(name, channel, author)
                await ctx.reply(f'{name} adicionado(a) à lista dos gigantescos nbzaAYAYA')
            else:
                await ctx.reply(f'Adicione o nome da pessoa ou do objeto colossal após o comando nbzaPalhacinha')

    @commands.command(name='anão', aliases=['anao'])
    @commands.cooldown(1, 1)
    async def anao(self, ctx: commands.Context):

        # twitch.tv/noobzinha
        if ctx.channel.name == 'noobzinha' and ctx.author.is_mod:
            channel = ctx.channel.name
            message = ctx.message.content
            name = ' '.join(message.split()[1:])
            if name != '':
                await mod.del_list(name, channel)
                await ctx.reply(f'Groselha APARENTEMENTE é maior que {name} nbzaLUL')
            else:
                await ctx.reply(f'Gigantesco descomunal não encontradokkkk nbzaBuxin')

    @commands.command(name='gigantes', aliases=['gigas'])
    @commands.cooldown(1, 10)
    async def gigantes(self, ctx: commands.Context):

        # twitch.tv/noobzinha
        if ctx.channel.name == 'noobzinha':
            names = await mod.get_list(ctx.channel.name)
            list1 = ''
            listall = []
            a = 1
            for i in names:
                if len(list1)+len(i) < 400:
                    list1 = list1 + f'{a}º {i}, '
                else:
                    listall.append(list1)
                    list1 = f'{a}º {i}, '
                a += 1
            if len(listall) > 0:
                for i in range(len(listall)):
                    await ctx.channel.send(f'/me Lista de Pessoas/Coisas maiores que a XL nbzaAnotando (Pág. {i+1}): {listall[i]}')
            await ctx.channel.send(f'/me Lista de Pessoas/Coisas maiores que a XL nbzaAnotando (Pág. {len(listall)+1}): {list1} Total: {len(names)}')

    @commands.command(name='namorado', aliases=['namorada', 'namo'])
    @commands.cooldown(1, 1)
    async def namorado(self, ctx: commands.Context):
        channel = ctx.channel.name
        author = ctx.author.name
        message = ctx.message.content
        name = ' '.join(message.split()[1:])

        # twitch.tv/marinaetc
        if ctx.channel.name == 'marinaetc':
            if name != '':
                await mod.add_list(name, channel, author)
                await ctx.reply(f'{name} adicionado à lista de namorados da marinaetc.')
                return
            else:
                await ctx.reply(f'Adicione o nome do namorado após o comando')

        # twitch.tv/emylolz
        elif ctx.channel.name == 'emylolz':
            if name != '':
                await mod.add_list(name, channel, author)
                await ctx.reply(f'{name} adicionada à lista de namoradas da emy.')
                return
            else:
                await ctx.reply(f'Adicione o nome da namorada após o comando')

        # twitch.tv/kiiaraw
        elif ctx.channel.name == 'kiiaraww':
            if name != '':
                await mod.add_list(name, channel, author)
                await ctx.reply(f'{name} adicionada à lista de namoradas da kiara.')
                return
            else:
                await ctx.reply(f'Adicione o nome da namorada após o comando')

    @commands.command(name='divorcio')
    @commands.cooldown(1, 1)
    async def divorcio(self, ctx: commands.Context):
        message = ctx.message.content
        name = ' '.join(message.split()[1:])
        channel = ctx.channel.name

        # twitch.tv/marinaetc
        if ctx.channel.name == 'marinaetc' and ctx.author.is_mod:
            if name != '':
                await mod.del_list(name, channel)
                await ctx.reply(f'Marina Reticências divorciou-se de {name}.')
            else:
                await ctx.reply(f'Namorado não encontradokkkk')

        # twitch.tv/emylolz
        elif ctx.channel.name == 'emylolz' and ctx.author.is_mod:
            if name != '':
                await mod.del_list(name, channel)
            else:
                await ctx.reply(f'Namorada não encontradakkkk')

        # twitch.tv/kiiaraww
        elif ctx.channel.name == 'kiiaraww' and ctx.author.is_mod:
            if name != '':
                await mod.del_list(name, channel)
            else:
                await ctx.reply(f'Namorada não encontradakkkk')

    @commands.command(name='namorados', aliases=['namoradas', 'namos'])
    @commands.cooldown(1, 10)
    async def namorados(self, ctx: commands.Context):

        # twitch.tv/marinaetc
        if ctx.channel.name == 'marinaetc':
            names = await mod.get_list(ctx.channel.name)
            list1 = ''
            listall = []
            a = 1
            for i in names:
                if len(list1)+len(i) < 455:
                    list1 = list1 + f'{a}º {i}, '
                else:
                    listall.append(list1)
                    list1 = f'{a}º {i}, '
                a += 1
            if len(listall) > 0:
                for i in range(len(listall)):
                    await ctx.channel.send(f'/me Namorados da Etc (Pág. {i+1}): {listall[i]}')
            await ctx.channel.send(f'/me Namorados da Etc (Pág. {len(listall)+1}): {list1} Total: {len(names)}')

        # twitch.tv/emylolz
        elif ctx.channel.name == 'emylolz':
            names = await mod.get_list(ctx.channel.name)
            list1 = ''
            listall = []
            a = 1
            for i in names:
                if len(list1)+len(i) < 455:
                    list1 = list1 + f'{a}ª {i}, '
                else:
                    listall.append(list1)
                    list1 = f'{a}ª {i}, '
                a += 1
            if len(listall) > 0:
                for i in range(len(listall)):
                    await ctx.channel.send(f'/me Namoradas da Emy (Pág. {i+1}): {listall[i]}')
            await ctx.channel.send(f'/me Namoradas da Emy (Pág. {len(listall)+1}): {list1} Total: {len(names)}')

        # twitch.tv/kiiaraww
        elif ctx.channel.name == 'kiiaraww':
            names = await mod.get_list(ctx.channel.name)
            list1 = ''
            listall = []
            a = 1
            for i in names:
                if len(list1)+len(i) < 455:
                    list1 = list1 + f'{a}ª {i}, '
                else:
                    listall.append(list1)
                    list1 = f'{a}ª {i}, '
                a += 1
            if len(listall) > 0:
                for i in range(len(listall)):
                    await ctx.channel.send(f'/me Namoradas da Mawasa (Pág. {i+1}): {listall[i]}')
            await ctx.channel.send(f'/me Namoradas da Mawasa (Pág. {len(listall)+1}): {list1} Total: {len(names)}')

    # Entra no canal que enviou a mensagem
    @commands.command(name='join', aliases=['entrar'])
    async def command_join(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor == BOT_NICK:
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor in await mod.get_channels():
                await ctx.send(f'/me Bot JÁ ESTÁ no canal {autor}')
            else:
                if len(await mod.get_channels()) < 20:
                    await mod.add_channel(autor)
                    await bot.join_channels([autor])
                    await ctx.send(f'/me Bot ENTROU no canal {autor}')
                else:
                    await ctx.send(f'/me No momento não temos vaga :( @1bode tá tentando resolver!')

    # Sai do canal que enviou a mensagem
    @commands.command(name='leave', aliases=['sair'])
    async def command_leave(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor == BOT_NICK:
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor not in await mod.get_channels():
                await ctx.send(F'/me Bot NÃO ESTÁ no canal {autor}')
            else:
                await mod.del_channel(autor)
                await ctx.send(F'/me Bot SAIU do canal {autor}')

    # Comando para git pull pelo chat
    @commands.command(name="update")
    async def update(self, ctx: commands.Context):
        if ctx.author.name == BOT_NICK:
            await ctx.send('Atualizando.')
            os.system("/usr/bin/git pull")
            print("Atualizando e reiniciando...")
            os.system("python3 main.py")
            exit()

    @commands.command(name='ping')
    @commands.cooldown(1, 3)
    async def ping(self, ctx: commands.Context):
        await ctx.reply('pong booudeHMM')


bot = Bot()
