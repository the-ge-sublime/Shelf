#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# File name: __init__.py
# Created:   2024-03-31 21:00
# @author    Gabriel Tenita <dev2023@tenita.eu>
# @link      https://github.com/the-ge/
# @copyright Copyright (c) 2024-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0


import sublime
from .core.version import __version__, sublimetext_build_min

if int(sublime.version()) < sublimetext_build_min:
    raise RuntimeError('Shelf only works with Sublime Text build ' + str(sublimetext_build_min) + ' or later.')
