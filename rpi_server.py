#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask


IS_AVAILABLE = None
app = Flask(__name__)


@app.route('/')
def index():
    if IS_AVAILABLE is None:
        return "Not installed yet"
    elif IS_AVAILABLE:
        return "Door is open"
    else:
        return "Door is locked"


@app.route('/register/<int:status>')
def set_status(status):
    global IS_AVAILABLE
    if status == 1:
        IS_AVAILABLE = True
    elif status == 0:
        IS_AVAILABLE = False
    elif status == -1:
        IS_AVAILABLE = None
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
