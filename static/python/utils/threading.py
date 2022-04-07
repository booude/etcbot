import threading
import time
import asyncio

from random import choice


def callback(self, func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func)
    loop.close()


async def prizes(self, message, resultado, prizes, ganhador):
    time.sleep(15)
    await message.channel.send(f'/me {ganhador}, você ganhou....... {resultado}')
    if resultado == prizes['7']['prize']:
        points = prizes['7']['points']
        await message.channel.send(f'!addpoints {ganhador} {points}')


async def autotweet(self, message, msglist, tweetapi):
    if len(msglist) > 500:
        tweet = choice(msglist)
        msglist.clear()
        time.sleep(30)
        content = f'{tweet["msg"]} (Aleatório de {tweet["autor"]}) #Choke7'
        tweetapi.update_status(status=content)
        id = tweetapi.user_timeline(count=1)[0]
        await message.channel.send(f'/me Tweet aleatório de @{tweet["autor"]} pode ser visto em: twitter.com/choke7chat/status/{id.id}')


def thread_create(self, threaded, *args, **kwargs):
    if threaded == 'prizes':
        threading.Thread(target=callback, args=(self, prizes(
            self, *args, **kwargs),)).start()
    if threaded == 'autotweet':
        threading.Thread(target=callback, args=(self, autotweet(
            self, *args, **kwargs),)).start()
