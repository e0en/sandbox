#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


root_dir = '.'
exclude_list = [
    'dotfiles',
    'Library',
]

exclude_list = [os.path.join(root_dir, x) for x in exclude_list]

for root, subdirs, files in os.walk(root_dir):
    n_exclude = sum([root.startswith(x) for x in exclude_list])
    n_hidden = sum([x.startswith('.') and len(x) > 1 for x in root.split('/')])
    if n_hidden == 0 and n_exclude == 0:
        for subdir in subdirs:
            for filename in files:
                file_path = os.path.join(root, subdir, filename)
