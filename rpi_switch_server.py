#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import dateutil.parser

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toilet.db'
db = SQLAlchemy(app)


class ToiletLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    time = db.Column(db.DateTime)  # in UTC time
    send_time = db.Column(db.DateTime)  # in UTC time

    def __init__(self, is_open, send_time):
        self.time = datetime.utcnow()
        self.send_time = send_time
        self.is_open = is_open

    def __repr__(self):
        if self.is_open:
            status_str = 'OPEN'
        else:
            status_str = 'LOCKED'
        return '<Toilet Log: %s [%s]>' % (self.time.isoformat(), status_str)

    def __str__(self):
        return self.__repr__()


class ToiletClientAliveLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)  # in UTC time
    send_time = db.Column(db.DateTime)  # in UTC time

    def __init__(self, send_time):
        self.time = datetime.utcnow()
        self.send_time = send_time

    def __repr__(self):
        return '<Client Alive Log: %s>' % self.time.isoformat()

    def __str__(self):
        return self.__repr__()


def seconds_since_log(log):
    return int(datetime.utcnow() - log.time)


@app.route('/init_db/')
def init_db():
    db.create_all()
    return 'db init OK'


@app.route('/')
def index():
    last_log = ToiletLog.query.order_by('-id').first()
    last_alive_log = ToiletClientAliveLog.query.order_by('-id').first()

    msg_str = ''
    if last_log is None:
        msg_str += 'Not recorded yet :('
    elif last_log.is_open:
        msg_str += "Door is open"
    else:
        locked_minutes = seconds_since_log(last_log) / 60
        msg_str += "Door is locked for %d minutes" % locked_minutes

    if last_alive_log is not None:
        alive_seconds = seconds_since_log(last_alive_log)
        msg_str += '<br />last alive msg %d seconds ago' % alive_seconds

    return msg_str


@app.route('/register/<int:status>/<string:send_time_str>')
def set_status(status, send_time_str):
    send_time = dateutil.parser.parse(send_time_str)
    if status == 1:
        new_log = ToiletLog(True, send_time)
    elif status == 0:
        new_log = ToiletLog(False, send_time)

    db.session.add(new_log)
    db.session.commit()
    return 'OK'


@app.route('/client_alive/<string:send_time_str>')
def client_alive(send_time_str):
    send_time = dateutil.parser.parse(send_time_str)
    new_log = ToiletClientAliveLog(send_time)

    db.session.add(new_log)
    db.session.commit()
    return 'OK'


@app.route('/log')
def show_log():
    logs = ToiletLog.query.order_by('-id')
    log_str = ''
    for log in logs:
        status_str = 'OPEN' if log.is_open else 'LOCK'
        log_str += '[status: %s]' % status_str
        log_str += '[sent: %s]' % log.send_time.isoformat()
        log_str += '[received: %s]' % log.time.isoformat()
        log_str += '<br />\n'
    print log_str
    return log_str


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
