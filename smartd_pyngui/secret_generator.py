#! /usr/bin/env python
#  -*- coding: utf-8 -*-

from scrambledconfigparser import ScrambledConfigParser

python_header = '#! /usr/bin/env python\n' \
                 '# -*- coding: utf-8 -*-\n\n'

c = ScrambledConfigParser()
key = c.generate_key()

body = 'AES_ENCRYPTION_KEY = %s' % key

with open('aes_key.py', 'w') as fp:
    fp.write(python_header)
    fp.write(body)