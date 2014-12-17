#!/usr/bin/env python
# -*- coding: utf-8 -*-
import private
import email
import imaplib
import re
import mechanize


def get_funshop_emails():
    # connect to gmail
    mail_client = imaplib.IMAP4_SSL('imap.gmail.com')
    mail_client.login('e0engoon@gmail.com', private.GMAIL_PASSWORD)

    rv, mailboxes = mail_client.list()
    mail_client.select()

    # fetch unread mails in inbox sent from funshop
    _, data = mail_client.search(None, '(FROM "no_reply@funshop.co.kr")')
    for mail_id in data[0].split():
        _, raw_message = mail_client.fetch(mail_id, '(RFC822)')
        message = email.message_from_string(raw_message[0][1])
        content = message.get_payload(decode=True)
        yield content
        # TODO: mark the email as read


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
    for content in get_funshop_emails():
        url = get_delivery_point_urls(content)
        is_success = get_delivery_point(url)
        print is_success
