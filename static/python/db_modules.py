from app import Base, Broadcaster, List, async_session, engine
from sqlalchemy.future import select


async def get_channels():
    channels = []
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(Broadcaster.is_active == True)
        result = await session.execute(query)
        for i in result.scalars():
            channels.append(i.twitch_id)
    await engine.dispose()
    return channels


async def add_channel(value):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(
            Broadcaster.twitch_id == value, Broadcaster.is_active == False)
        result = await session.execute(query)
        channel = result.scalars().first()
        if channel:
            channel.is_active = True
        else:
            session.add(Broadcaster(twitch_id=value))
        await session.commit()
    await engine.dispose()


async def del_channel(value):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(
            Broadcaster.twitch_id == value, Broadcaster.is_active == True)
        result = await session.execute(query)
        channel = result.scalars().first()
        if channel:
            channel.is_active = False
        await session.commit()
    await engine.dispose()


async def get_list(channel):
    names = []
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(List).where(List.broadcaster_id ==
                                       id, List.is_active == True)
        result = await session.execute(query)
        for i in result.scalars():
            names.append(i.name)
    await engine.dispose()
    return names


async def add_list(name, channel, creator):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(List).where(
                List.name == name, List.is_active == False, List.broadcaster_id == id)
            result = await session.execute(query)
            item = result.scalars().first()
            if item:
                item.is_active = True
            else:
                session.add(
                    List(name=name, created_by=creator, broadcaster_id=id))
            await session.commit()
        await engine.dispose()


async def del_list(name, channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(List).where(
                List.name == name, List.is_active == True, List.broadcaster_id == id)
            result = await session.execute(query)
            item = result.scalars().first()
            if item:
                item.is_active = False
            await session.commit()
        await engine.dispose()
