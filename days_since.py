#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

d_begin = datetime(2011, 7, 17)
d_now = datetime.now()

diff = d_now - d_begin
print(diff.days + 1)
