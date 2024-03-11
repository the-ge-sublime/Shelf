# -*- coding: UTF-8 -*-

import sublime

min_version = 4085
if int(sublime.version()) < min_version:
    raise RuntimeError(f'Shelf works with Sublime Text build {min_version}+ only.')
