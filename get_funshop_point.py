#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gmail import Gmail
import os
import time
import datetime
import re
import mechanicalsoup
import private.keys as private


def get_delivery_point_urls(content):
    # extract delivery point hyperlink from the email content
    link_pattern = b'href="(https+://www.funshop.co.kr/member/login[^"]+)"'
    link_pattern = re.compile(link_pattern)
    url = None
    for link_match in link_pattern.finditer(content):
        url = link_match.group(1)
    return url


def get_delivery_point(url):
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_verbose(2)
    browser.set_debug(True)
    # open the hyperlink
    resp = browser.open(url)
    browser.add_soup(resp, soup_config={'features': 'lxml'})
    soup = resp.soup

    # log-in to funshop
    for i_form, form in enumerate(soup.select('form')):
        if form.attrs['id'].lower() == 'frmlogin':
            form_id = form.attrs['id']
            break
    form = browser.select_form(selector='#' + form_id)
    print(f'chose form {form_id}')

    form['Account'] = 'e0en'
    form['Password'] = private.FUNSHOP_PASSWORD
    submit_button = soup.select('#btnSubmit')[0]
    form.choose_submit(submit_button)
    print(f'chose submit button {submit_button}')

    browser.submit_selected()
    # check if the process was succeeded
    success_urls = [
            'https://www.funshop.co.kr/myfunroom/artpoint',
            'https://www.funshop.co.kr/goods/savedpoint']
    p = browser.get_current_page()
    browser_url = browser.get_url()
    for url in success_urls:
        if browser_url.startswith(url):
            return True
    return False


if __name__ == '__main__':
    dir_here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_here, 'private/funshop_result.txt')
    g = Gmail()
    while not g.logged_in:
        time.sleep(1)
        g.login(private.GMAIL_ID, private.GMAIL_PASSWORD)
    print("logged in!")
    mails = g.inbox().mail(unread=True, sender='no_reply@funshop.co.kr')
    print("total %d unread mails from funshop" % len(mails))

    for m in mails:
        m.fetch()
        content = m.message.get_payload(decode=True)
        url = get_delivery_point_urls(content)
        if url is None:
            print('No point button on this email')
            is_success = True
        else:
            is_success = get_delivery_point(url)
        with open(filename, 'a') as fp:
            fp.write('%s: %s\n' % (datetime.datetime.now().isoformat(), is_success))
        if is_success:
            print('success!')
            m.read()
            m.archive()
            m.remove_label("\\Important")
        else:
            print('failed!')
    if len(mails) == 0:
        with open(filename, 'a') as fp:
            fp.write('%s: no mail\n' % datetime.datetime.now().isoformat())
    g.logout()
