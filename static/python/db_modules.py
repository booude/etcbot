from app import db, Broadcaster, Prize, List


def get_channels():
    CHANNELS = []
    for i in range(len(db.session.query(Broadcaster.twitch_id).where(Broadcaster.is_active == True).all())):
        CHANNELS.append(db.session.query(Broadcaster.twitch_id).where(
            Broadcaster.is_active == True).all()[i][0])
    return CHANNELS


def add_channel(value):
    if db.session.query(db.exists().where(Broadcaster.twitch_id == value, Broadcaster.is_active == False)).scalar():
        Broadcaster.query.filter_by(twitch_id=value, is_active=False).update({
            Broadcaster.is_active: True})
        db.session.commit()
        return
    else:
        db.session.add(Broadcaster(twitch_id=value))
        db.session.commit()
        return


def del_channel(value):
    if db.session.query(db.exists().where(Broadcaster.twitch_id == value, Broadcaster.is_active == True)).scalar():
        Broadcaster.query.filter_by(twitch_id=value, is_active=True).update({
            Broadcaster.is_active: False})
        db.session.commit()
        return


def get_list(channel):
    names = []
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()
    for i in range(len(db.session.query(List.name).where(List.broadcaster == b_id, List.is_active == True).all())):
        names.append(db.session.query(List.name).where(
            List.broadcaster == b_id, List.is_active == True).all()[i][0])
    return names


def add_list(name, channel, creator):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()
    if db.session.query(db.exists().where(List.name == name, List.is_active == False, List.broadcaster == b_id)).scalar():
        List.query.filter_by(name=name, is_active=False).update({
            List.is_active: True})
        db.session.commit()
        return
    else:
        db.session.add(List(name=name, broadcaster=b_id, created_by=creator))
        db.session.commit()
        return


def del_list(name, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()
    if db.session.query(db.exists().where(List.name == name, List.is_active == True, List.broadcaster == b_id)).first():
        List.query.filter_by(name=name, is_active=True).update({
            List.is_active: False})
        db.session.commit()
        return


def add_prize(name, prize, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()
    db.session.add(Prize(name=name, prize=prize, broadcaster=b_id))
    db.session.commit()
    return
