import app


def get_channels():
    CHANNELS = []
    for i in range(len(app.db.session.query(app.Broadcaster.twitch_id).where(app.Broadcaster.is_active == True).all())):
        CHANNELS.append(app.db.session.query(app.Broadcaster.twitch_id).where(
            app.Broadcaster.is_active == True).all()[i][0])
    return CHANNELS


def add_channel(value):
    if app.db.session.query(app.db.exists().where(app.Broadcaster.twitch_id == value, app.Broadcaster.is_active == False)).scalar():
        app.Broadcaster.query.filter_by(twitch_id=value, is_active=False).update({
            app.Broadcaster.is_active: True})
        app.db.session.commit()
        return
    else:
        app.db.session.add(app.Broadcaster(twitch_id=value))
        app.db.session.commit()
        return


def del_channel(value):
    if app.db.session.query(app.db.exists().where(app.Broadcaster.twitch_id == value, app.Broadcaster.is_active == True)).scalar():
        app.Broadcaster.query.filter_by(twitch_id=value, is_active=True).update({
            app.Broadcaster.is_active: False})
        app.db.session.commit()
        return


def get_list(channel):
    names = []
    b_id = app.db.session.query(app.Broadcaster).where(
        app.Broadcaster.twitch_id == channel).first()
    for i in range(len(app.db.session.query(app.List.name).where(app.List.broadcaster == b_id, app.List.is_active == True).all())):
        names.append(app.db.session.query(app.List.name).where(
            app.List.broadcaster == b_id, app.List.is_active == True).all()[i][0])
    return names


def add_list(name, channel, creator):
    b_id = app.db.session.query(app.Broadcaster).where(
        app.Broadcaster.twitch_id == channel).first()
    if app.db.session.query(app.db.exists().where(app.List.name == name, app.List.is_active == False, app.List.broadcaster == b_id)).scalar():
        app.List.query.filter_by(name=name, is_active=False).update({
            app.List.is_active: True})
        app.db.session.commit()
        return
    else:
        app.db.session.add(
            app.List(name=name, broadcaster=b_id, created_by=creator))
        app.db.session.commit()
        return


def del_list(name, channel):
    b_id = app.db.session.query(app.Broadcaster).where(
        app.Broadcaster.twitch_id == channel).first()
    if app.db.session.query(app.db.exists().where(app.List.name == name, app.List.is_active == True, app.List.broadcaster == b_id)).first():
        app.List.query.filter_by(name=name, is_active=True).update({
            app.List.is_active: False})
        app.db.session.commit()
        return


def add_prize(name, prize, channel):
    b_id = app.db.session.query(app.Broadcaster).where(
        app.Broadcaster.twitch_id == channel).first()
    app.db.session.add(app.Prize(name=name, prize=prize, broadcaster=b_id))
    app.db.session.commit()
    return
