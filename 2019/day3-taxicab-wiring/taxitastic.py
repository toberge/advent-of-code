#!/usr/bin/env python3

import os

fd = os.open('./input', os.O_RDONLY)
wired = os.read(fd, 2900)

wired = wired.split(sep='')

print('hi there')
