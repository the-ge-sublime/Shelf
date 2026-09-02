#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# File name: main.py
# Created:   2024-03-11 09:24
# @author    Gabriel Tenita <dev2023@tenita.eu>
# @link      https://github.com/the-ge/
# @copyright Copyright (c) 2024-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0

import sublime_plugin

from .core.renderer import Renderer
from .core.shelf import CommonShelf, ProjectShelf

#from Shelf.core.debug import _d


def get_shelf(name):
    shelves = {
        "common": CommonShelf,
        "project": ProjectShelf,
    }

    try:
        return shelves[name]()
    except KeyError:
        raise ValueError(f"Unknown shelf: {name}") from None


class ShelfCommand(sublime_plugin.WindowCommand):
    """Common helpers shared by all shelf commands."""

    def render(self):
        view = self.window.active_view()
        return Renderer().render_shelves(view.style()["foreground"])

    def refresh_popup(self):
        self.window.active_view().update_popup(self.render())


class ShelfViewCommand(ShelfCommand):
    def run(self):
        self.show_popup(self.render())

    def show_popup(self, content):
        view = self.window.active_view()

        width, height = view.viewport_extent()
        location = view.visible_region().a

        view.show_popup(
            content=content,
            location=location,
            on_navigate=self.on_navigate,
            max_width=width,
            max_height=height,
            # flags=sublime.KEEP_ON_SELECTION_MODIFIED,
        )

    def on_navigate(self, href):
        if href == "#":
            self.window.active_view().hide_popup()


class ShelfAddCommand(ShelfCommand):
    def run(self, shelf):
        item = self.window.active_view().file_name()
        if not item:
            return

        get_shelf(shelf).add(item)


class ShelfItemMoveUpCommand(ShelfCommand):
    def run(self, item, shelf):
        get_shelf(shelf).move_up(tuple(item))
        self.refresh_popup()


class ShelfItemMoveDownCommand(ShelfCommand):
    def run(self, item, shelf):
        get_shelf(shelf).move_down(tuple(item))
        self.refresh_popup()


class ShelfItemRemoveCommand(ShelfCommand):
    def run(self, shelf, item):
        get_shelf(shelf).remove(tuple(item))
        self.refresh_popup()
