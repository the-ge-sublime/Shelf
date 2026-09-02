# File name: renderer.py
# Created:   2024-03-11 09:24
# @author    Gabriel Tenita <g1704578400@tenita.eu@tenita.eu>
# @see       https://github.com/the-ge/
# @copyright Copyright (c) 2026-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0
#
# See also https://www.sublimetext.com/docs/minihtml.html.

from __future__ import annotations

import math
from pathlib import Path

import sublime
from Shelf.core.shelf import CommonShelf, ProjectShelf


class Renderer:
    RAW_SRC = "Packages/Shelf/assets"
    ACTION_CLASS = "btn action-btn"
    DISABLED_CLASS = "btn disabled-btn"

    def __init__(self, foreground_hex: str) -> None:
        self.color_scheme = self.get_color_scheme(foreground_hex)

    def render_shelves(self) -> str:

        common_html, common_width = self.render_shelf(CommonShelf())

        project_html = ""
        title_width = common_width

        if sublime.active_window().project_file_name():
            project_html, project_width = self.render_shelf(ProjectShelf())
            title_width = max(title_width, project_width)

        title_rems = math.ceil(title_width) * 0.75
        actions_rems = 12
        caption_actions_rems = 9.25

        css = sublime.load_resource(
            f"{self.RAW_SRC}/css/shelf.css"
        ).strip()

        return f"""<style>
{css}

html {{
  --body-width: {title_rems + actions_rems + 2}rem;
  --title-width: {title_rems}rem;
  --actions-width: {actions_rems}rem;
  --caption-actions-width: {caption_actions_rems}rem;
}}
</style>

<body id="shelf-popup">

    <div class="close">
        <a href="#" class="close-btn btn">
            {self.icon('close')}
        </a>
    </div>

    {project_html}
    {common_html}

</body>
"""

    def render_shelf(self, shelf: CommonShelf | ProjectShelf) -> tuple[str, str, str]:
        items = shelf.read_inventory()
        shelf_title_suffix = '&nbsp;' * (8 - len(shelf.key))
        rendered = f"""
    <div class="table">

        <div class="th row">
            {shelf.key.upper()}{shelf_title_suffix}
            <div class="actions">
                {self.render_open_file_action(
                    shelf.file.as_posix(),
                    self.icon("edit"),
                    "title no-underline",
                )}
            </div>
        </div>
"""
        max_len = 0
        for index, (name, path) in enumerate(items):
            row_class = "row-even" if index % 2 == 0 else "row-odd"

            rendered += f"""
        <div class="row {row_class}">
            {self.render_open_file_action(path, name, "title no-underline")}
            <div class="actions">
                {self.side_actions(
                    shelf.key,
                    (name, path),
                    index,
                    len(items),
                )}
            </div>
        </div>
"""

            max_len = max(max_len, len(name))

        rendered += """
    </div>
"""

        return rendered, max_len

    def side_actions(
        self,
        shelf: CommonShelf | ProjectShelf,
        item: list,
        index: int,
        count: int,
    ) -> str:
        args = {
            "shelf": shelf,
            "item": item,
        }
        path = Path(item[1]).parent.as_posix()

        return (
            self.render_action(f"Edit {path}", "open_dir", {"dir": path}, "folder")
            + self.render_move_action("up", args, index, count)
            + self.render_move_action("down", args, index, count)
            + self.render_action("Remove", "shelf_item_remove", args, "trash")
        )

    def icon(self, name: str) -> str:
        return (
            f'<img class="btn-icon" '
            f'src="res://{self.RAW_SRC}/img/{name}-{self.color_scheme}.png">'
        )

    def render_open_file_action(self, path: str, text: str, css_class: str) -> str:
        return self.render_link(
            f"Edit {path}",
            "open_file",
            {
                "file": path,
                "content": f"Could not open {path}",
            },
            text,
            css_class,
        )

    def render_move_action(
        self,
        direction: str,
        args: dict[str, str],
        index: int,
        count: int,
    ) -> str:
        enabled = {
            'up': index > 0,
            'down': index < count - 1,
        }

        return self.render_link(
            f"Move {direction}",
            f"shelf_item_move_{direction}",
            args,
            self.icon(f"arrow-{direction}"),
            self.ACTION_CLASS,
        ) if enabled[direction] else self.render_link("", "", args, "&nbsp;", self.DISABLED_CLASS)

    def render_action(
        self,
        title: str,
        command: str,
        args: dict[str, str],
        icon: str,
    ) -> str:
        return self.render_link(
            title,
            command,
            args,
            self.icon(icon),
            self.ACTION_CLASS,
        )

    @staticmethod
    def render_link(
        title: str,
        command: str,
        args: dict[str, str],
        text: str,
        css_class: str = "",
    ) -> str:
        href = "subl:" + sublime.html_format_command(command, args)
        css = f' class="{css_class}"' if css_class else ""

        return (
            f'<a href="{href}"{css} '
            f'title="{title}">{text}</a>'
        )

    @staticmethod
    def get_color_scheme(foreground_hex: str) -> str:
        foreground_hex = foreground_hex.lstrip("#")
        rgb = tuple(
            int(foreground_hex[i : i + 2], 16)
            for i in (0, 2, 4)
        )

        return "dark" if rgb > (127, 127, 127) else "light"
