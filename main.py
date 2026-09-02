# File name: main.py
# Created:   2024-03-11 09:24
# @author    Gabriel Tenita <dev2023@tenita.eu>
# @link      https://github.com/the-ge/
# @copyright Copyright (c) 2024-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0

from __future__ import annotations

import sublime
import sublime_plugin

from .core.renderer import Renderer
from .core.shelf import CommonShelf, ProjectShelf
from .core.version import sublimetext_build_min

if int(sublime.version()) < sublimetext_build_min:
    msg = f"Shelf only works with Sublime Text build {sublimetext_build_min!s} or later."
    raise RuntimeError(msg)


def get_shelf(name: str) -> CommonShelf | ProjectShelf:
    shelves = {
        "common": CommonShelf,
        "project": ProjectShelf,
    }

    try:
        return shelves[name]()
    except KeyError:
        msg = f"Unknown shelf: {name}"
        raise ValueError(msg) from None


class ShelfCommand(sublime_plugin.WindowCommand):
    """Common helpers shared by all shelf commands."""

    def render(self) -> str:
        view = self.window.active_view()
        return Renderer().render_shelves(view.style()["foreground"])

    def refresh_popup(self) -> None:
        self.window.active_view().update_popup(self.render())


class ShelfViewCommand(ShelfCommand):
    def run(self) -> None:
        self.show_popup(self.render())

    def show_popup(self, content: str) -> None:
        view = self.window.active_view()

        width, height = view.viewport_extent()
        location = view.visible_region().a

        view.show_popup(
            content=content,
            location=location,
            on_navigate=self.on_navigate,
            max_width=width,
            max_height=height,
        )

    def on_navigate(self, href: str) -> None:
        if href == "#":
            self.window.active_view().hide_popup()


class ShelfAddCommand(ShelfCommand):
    def run(self, shelf: CommonShelf | ProjectShelf) -> None:
        item = self.window.active_view().file_name()
        if not item:
            return

        get_shelf(shelf).add(item)


class ShelfItemMoveUpCommand(ShelfCommand):
    def run(self, shelf: str, item: list[str, str]) -> None:
        get_shelf(shelf).move_up(tuple(item))
        self.refresh_popup()


class ShelfItemMoveDownCommand(ShelfCommand):
    def run(self, shelf: str, item: list[str, str]) -> None:
        get_shelf(shelf).move_down(tuple(item))
        self.refresh_popup()


class ShelfItemRemoveCommand(ShelfCommand):
    def run(self, shelf: str, item: list[str, str]) -> None:
        get_shelf(shelf).remove(tuple(item))
        self.refresh_popup()
