import threading
import time
import asyncio

from random import choice


def callback(self, func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func)
    loop.close()


async def autotweet(self, message, msglist, tweetapi):
    if len(msglist) > 300:
        tweet = choice(msglist)
        msglist.clear()
        time.sleep(30)
        content = f'{tweet["msg"]} (Aleatório de {tweet["autor"]}) #Choke7'
        tweetapi.update_status(status=content)
        id = tweetapi.user_timeline(count=1)[0]
        await message.channel.send(f'/me Tweet aleatório de @{tweet["autor"]} pode ser visto em: twitter.com/choke7chat/status/{id.id}')


def thread_create(self, func, *args, **kwargs):
    t = threading.Thread(target=callback, args=(self, func(
        self, *args, **kwargs), ))
    t.start()
