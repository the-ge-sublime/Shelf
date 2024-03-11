# -*- coding: UTF-8 -*-
# [TODO]
# - convert PNGs to data URIs and change their color with Python
# - tab context menu
# - headers buttons
#   - open the shelf files
#   - delete the shelf files
# - hide header when no shelf file
# - hover? (sublime_plugin.EventListener.in_hover)
# [FIX]
# - set a min-width
# - detect when file is already opened and alert

import sublime
import sublime_plugin
from Shelf.core.shelf import CommonShelf, ProjectShelf
from Shelf.core.renderer import Renderer
#from Shelf.core.debug import _d


# version = 0.0.3


class ShelfViewCommand(sublime_plugin.WindowCommand):
    def run(self):
        foreground_hex = self.window.active_view().style()['foreground'].lstrip('#')
        foreground_rgb = tuple(int(foreground_hex[i:i+2], 16) for i in (0, 2, 4))
        color_scheme = 'dark' if foreground_rgb > (127, 127, 127) else 'light'

        self.show_popup(Renderer().render_shelves(color_scheme))

    def show_popup(self, text):
        view = self.window.active_view()
        max_width, max_height = view.viewport_extent()
        region = view.visible_region()
        view.show_popup(
            content=text,
            location=region.a,
            on_navigate=self.on_close_popup,
            max_height=max_height,
            max_width=max_width,
            # flags=sublime.KEEP_ON_SELECTION_MODIFIED
        )

    def on_close_popup(self, href):
        if href == '#':
            self.window.active_view().hide_popup()


class ShelfAddCommand(sublime_plugin.WindowCommand):
    def run(self, shelf):
        if shelf != 'project' and shelf != 'common':
            raise TypeError('Unknown <' + shelf + '> shelf')
        shelf = CommonShelf() if shelf == 'common' else ProjectShelf()

        item = self.window.active_view().file_name()
        if item:
            shelf.add(item)


class ShelfItemMoveUpCommand(sublime_plugin.WindowCommand):
    def run(self, item, shelf):
        item = tuple(item)

        if shelf != 'project' and shelf != 'common':
            raise TypeError('Unknown <' + shelf + '> shelf')

        shelf = CommonShelf() if shelf == 'common' else ProjectShelf()
        shelf.move_up(item)

        foreground_hex = self.window.active_view().style()['foreground'].lstrip('#')
        foreground_rgb = tuple(int(foreground_hex[i:i+2], 16) for i in (0, 2, 4))
        color_scheme = 'dark' if foreground_rgb > (127, 127, 127) else 'light'
        self.window.active_view().update_popup(Renderer().render_shelves(color_scheme))


class ShelfItemMoveDownCommand(sublime_plugin.WindowCommand):
    def run(self, item, shelf):
        item = tuple(item)

        if shelf != 'project' and shelf != 'common':
            raise TypeError('Unknown <' + shelf + '> shelf')

        shelf = CommonShelf() if shelf == 'common' else ProjectShelf()
        shelf.move_down(item)

        foreground_hex = self.window.active_view().style()['foreground'].lstrip('#')
        foreground_rgb = tuple(int(foreground_hex[i:i+2], 16) for i in (0, 2, 4))
        color_scheme = 'dark' if foreground_rgb > (127, 127, 127) else 'light'
        self.window.active_view().update_popup(Renderer().render_shelves(color_scheme))


class ShelfItemRemoveCommand(sublime_plugin.WindowCommand):
    def run(self, shelf, item):
        item = tuple(item)

        if shelf != 'project' and shelf != 'common':
            raise TypeError('Unknown <' + shelf + '> shelf')

        shelf = CommonShelf() if shelf == 'common' else ProjectShelf()
        shelf.remove(item)

        foreground_hex = self.window.active_view().style()['foreground'].lstrip('#')
        foreground_rgb = tuple(int(foreground_hex[i:i+2], 16) for i in (0, 2, 4))
        color_scheme = 'dark' if foreground_rgb > (127, 127, 127) else 'light'
        self.window.active_view().update_popup(Renderer().render_shelves(color_scheme))
