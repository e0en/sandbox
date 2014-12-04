#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pipes


def upgrade_pip():
    cmd = "pip freeze --local | grep -v '^\-e' | cut -d = -f 1" + \
        " | xargs pip install -U"
    os.system(cmd)


def clean_python_codes(root_dir, exclude_list):
    exclude_list = [os.path.join(root_dir, x) for x in exclude_list]
    for root, subdirs, files in os.walk(root_dir):
        n_exclude = sum([root.startswith(x) for x in exclude_list])
        n_hidden = sum([x.startswith('.') and len(x) > 1
                        for x in root.split('/')])
        if n_hidden == 0 and n_exclude == 0:
            for filename in files:
                file_path = pipes.quote(os.path.join(root, filename))
                if file_path.endswith('.py'):
                    print file_path
                    os.system('autopep8 -i %s' % file_path)
                elif file_path.endswith('.pyc'):
                    print file_path
                    os.system('rm %s' % file_path)


upgrade_pip()
clean_python_codes(os.path.expanduser('~'), ['dotfiles', 'Library'])
