# File name: renderer.py
# Created:   2024-03-11 09:24
# @author    Gabriel Tenita <g1704578400@tenita.eu@tenita.eu>
# @see       https://github.com/the-ge/
# @copyright Copyright (c) 2026-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0
#
# See also https://www.sublimetext.com/docs/minihtml.html.

import math
import os

import sublime

from Shelf.core.shelf import CommonShelf, ProjectShelf


class Renderer:
    RAW_SRC = "Packages/Shelf/assets"

    ACTION_CLASS = "btn action-btn"
    DISABLED_CLASS = "btn disabled-btn"

    def render_shelves(self, foreground_hex):
        color_scheme = self.get_color_scheme(foreground_hex)

        _, common_html, common_width = self.render_shelf(
            CommonShelf(), color_scheme
        )

        project_html = ""
        title_width = common_width

        if sublime.active_window().project_file_name():
            _, project_html, project_width = self.render_shelf(
                ProjectShelf(), color_scheme
            )
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
            {self.icon("close", color_scheme)}
        </a>
    </div>

    {project_html}
    {common_html}

</body>
"""

    def render_shelf(self, shelf, color_scheme):
        items = shelf.read()
        shelf_title_suffix = '&nbsp;' * (8 - len(shelf.key))
        rendered = f"""
    <div class="table">

        <div class="th row">
            {shelf.key.upper()}{shelf_title_suffix}
            <div class="actions">
                {self.render_open_file_action(
                    shelf.file,
                    self.icon("edit", color_scheme),
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
            {self.render_open_file_action(
                path,
                name,
                "title no-underline",
            )}
            <div class="actions">
                {self.side_actions(
                    (name, path),
                    shelf.key,
                    index,
                    len(items),
                    color_scheme,
                )}
            </div>
        </div>
"""

            max_len = max(max_len, len(name))

        rendered += """
    </div>
"""

        return shelf.file, rendered, max_len

    def side_actions(
        self,
        item,
        shelf,
        index,
        count,
        color_scheme,
    ):
        args = {
            "item": item,
            "shelf": shelf,
        }

        path = os.path.dirname(item[1])

        return (
            self.render_action(
                f"Edit {path}",
                "open_dir",
                {"dir": path},
                "folder",
                color_scheme,
            )
            + self.render_move_action(
                "up",
                args,
                index > 0,
                color_scheme,
            )
            + self.render_move_action(
                "down",
                args,
                index < count - 1,
                color_scheme,
            )
            + self.render_action(
                "Remove",
                "shelf_item_remove",
                args,
                "trash",
                color_scheme,
            )
        )

    def icon(self, name, color_scheme):
        return (
            f'<img class="btn-icon" '
            f'src="res://{self.RAW_SRC}/img/{name}-{color_scheme}.png">'
        )

    def render_open_file_action(self, path, text, css_class):
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
        direction,
        args,
        enabled,
        color_scheme,
    ):
        return self.render_link(
            f"Move {direction}" if enabled else "",
            f"shelf_item_move_{direction}" if enabled else "",
            args,
            self.icon(f"arrow-{direction}", color_scheme)
            if enabled
            else "&nbsp;",
            self.ACTION_CLASS if enabled else self.DISABLED_CLASS,
        )

    def render_action(
        self,
        title,
        command,
        args,
        icon,
        color_scheme,
    ):
        return self.render_link(
            title,
            command,
            args,
            self.icon(icon, color_scheme),
            self.ACTION_CLASS,
        )

    @staticmethod
    def render_link(title, command, args, text, css_class=""):
        href = "subl:" + sublime.html_format_command(command, args)
        css = f' class="{css_class}"' if css_class else ""

        return (
            f'<a href="{href}"{css} '
            f'title="{title}">{text}</a>'
        )

    @staticmethod
    def get_color_scheme(foreground_hex):
        foreground_hex = foreground_hex.lstrip("#")
        rgb = tuple(
            int(foreground_hex[i : i + 2], 16)
            for i in (0, 2, 4)
        )

        return "dark" if rgb > (127, 127, 127) else "light"
