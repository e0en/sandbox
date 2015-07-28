#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gmail import Gmail
import os
import time
import re
import mechanize
import private


def get_delivery_point_urls(content):
    # extract delivery point hyperlink from the email content
    link_pattern = 'href="(https+://www.funshop.co.kr/member/login[^"]+)"'
    link_pattern = re.compile(link_pattern)
    for link_match in link_pattern.finditer(content):
        url = link_match.group(1)
    return url


def get_delivery_point(url):
    browser = mechanize.Browser()
    # open the hyperlink
    browser.open(url)

    # log-in to funshop
    for i_form, form in enumerate(browser.forms()):
        if form.attrs['id'] == 'frmlogin':
            break
    browser.select_form(nr=i_form)
    browser['Account'] = 'e0en'
    browser['Password'] = private.FUNSHOP_PASSWORD
    browser.submit()

    # check if the process was succeeded
    success_url = 'https://www.funshop.co.kr/myfunroom/artpoint'
    return browser.geturl().startswith(success_url)


if __name__ == '__main__':
    dir_here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_here, 'private/funshop_result.txt')
    g = Gmail()
    while not g.logged_in:
        time.sleep(1)
        g.login(private.GMAIL_ID, private.GMAIL_PASSWORD)
    mails = g.inbox().mail(unread=True, sender='no_reply@funshop.co.kr')

    for m in mails:
        m.fetch()
        content = m.message.get_payload(decode=True)
        url = get_delivery_point_urls(content)
        is_success = get_delivery_point(url)
        with open(filename, 'a') as fp:
            fp.write('%s\n' % is_success)
        if is_success:
            m.read()
            m.archive()

    g.logout()
