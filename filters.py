#!/usr/bin/env python

import getpass
import optparse
import sys
import gdata.apps.emailsettings.client

APPNAME = 'abrody-filters-1'

class Client(object):
    def __init__(self, email, passwd):
        self.email = email
        self.user, self.domain = email.split('@')

        self.client = gdata.apps.emailsettings.client.EmailSettingsClient(
            domain=self.domain)
        self.client.ClientLogin(email=email, password=passwd, source=APPNAME)

    def create_filter(self, **kwargs):
        self.client.CreateFilter(self.user, **kwargs)

if __name__ == '__main__':
    extra = '''
EMAIL: your google account email address
ACTION: currently only 'create' is implemented
'''

    p = optparse.OptionParser(usage='%prog EMAIL ACTION [options]')
    p.add_option('-f', '--from-address', dest='from_address', metavar='ADDR',
                 help='filter by source email address')
    p.add_option('-t', '--to-address', dest='to_address', metavar='ADDR',
                 help='filter by destination email address')
    p.add_option('-w', '--has-word', dest='has_the_word', metavar='WORD',
                 help='word email must contain in subject or body')
    p.add_option('-n', '--not-has-word', dest='does_not_have_the_word',
                 metavar='WORD', help='exclude messages with this word')
    p.add_option('-A', '--has-attachments', dest='has_attachments',
                 action='store_true', help='filter messages with attachments')
    p.add_option('-N', '--no-attachments', dest='has_attachments',
                 action='store_false',
                 help='exclude messages with attachments')
    p.add_option('-l', '--label', dest='label',
                 help='name of the label to add to matching messages')
    p.add_option('-r', '--mark-read', dest='mark_as_read', action='store_true',
                 help='mark matching messages read')
    p.add_option('-a', '--archive', dest='archive', action='store_true',
                 help='archive matching messages')

    try:
        email = sys.argv[1]
        action = sys.argv[2]
    except IndexError:
        p.print_help()
        print extra
        sys.exit(1)

    opts, args = p.parse_args(sys.argv[3:])

    if action == 'create':
        passwd = getpass.getpass('password: ')
        c = Client(email, passwd)
        kwargs = {}
        for key in ['from_address', 'to_address', 'subject', 'has_the_word',
                    'does_not_have_the_word', 'has_attachments', 'label',
                    'mark_as_read', 'archive']:
            if hasattr(opts, key):
                kwargs[key] = getattr(opts, key)

        print 'creating filter with:', kwargs

        c.create_filter(**kwargs)
    else:
        p.error('unknown action, expected [create]')

