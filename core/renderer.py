# -*- coding: UTF-8 -*-
# https://www.sublimetext.com/docs/minihtml.html

import sublime
import os
import math
from Shelf.core.shelf import CommonShelf, ProjectShelf


class Renderer:
    action_clss = 'btn action-btn'
    disabled_clss = 'btn disabled-btn'

    def render_shelves(self, color_scheme):
        self.color_scheme = color_scheme

        project_shelf_file, project_shelf_items, prject_max_len = self.render_shelf(ProjectShelf())
        common_shelf_file, common_shelf_items, common_max_len = self.render_shelf(CommonShelf())
        # make up for the lack of table support in minihtml
        # by calculating the file names column length using a totally magic factor
        title_rems = math.ceil(max(prject_max_len, common_max_len) * 0.675)
        actions_rems = 12
        css = (
            '<style>\n'
            + sublime.load_resource('Packages/Shelf/assets/css/shelf.css').strip()
            + '\n\n'
            + 'html {\n'
            + '  --body-width: ' + str(title_rems + actions_rems + 2) + 'rem;\n'
            + '  --title-width: ' + str(title_rems) + 'rem;\n'
            + '  --actions-width: ' + str(actions_rems) + 'rem;\n'
            + '}\n'
            + '</style>\n'
        )

        return (
            '\n'
            + '<body id="shelf-popup">\n'
            + css
            + '    <div class="close">\n'
            + '        <a href="#" class="close-btn btn"><img class="btn-icon" src="res://Packages/Shelf/assets/img/close-' + self.color_scheme + '.png"></a>'
            + '    </div>\n'
            + '    <div class="table">\n'
            + project_shelf_items
            + '    </div>\n'
            + '    <div class="table">\n'
            + common_shelf_items
            + '    </div>\n'
            + '    </body>'
        )

    def render_shelf(self, shelf):
        rendered = (
            '        <div class="row">\n'
            + '            <h4 class="title">' + shelf.key.upper() + '</h4>\n'
            + '            <div class="actions">' + self.render_open_file_action(shelf.file, self.icon('edit'), self.action_clss) + '</div>\n'
            + '        </div>\n'
        )

        items = shelf.read()
        max_len, is_odd, k, count = 0, False, 0, len(items)
        while k < count:
            name, path = item = items[k]
            alt_class = 'row-' + ('odd' if is_odd else 'even')
            is_movable = (k > 0) and (k < count)
            rendered += (
                '        <div class="row ' + alt_class + '">\n'
                + '            ' + self.render_open_file_action(path, name, 'title no-underline') + '\n'
                + '            <div class="actions">' + self.side_actions(item, shelf.key, k, count) + '</div>\n'
                + '        </div>\n'
            )
            max_len = max(max_len, len(name))
            is_odd = not is_odd
            k += 1

        return shelf.file, rendered, max_len

    def side_actions(self, item, shelf, index, count):
        args = {'item': item, 'shelf': shelf}
        path = os.path.dirname(item[1])

        return (
            self.render_action('Open ' + path, 'open_dir', {'dir': path}, 'folder')
            + self.render_move_action('up', args, index > 0)
            + self.render_move_action('down', args, index < count - 1)
            + self.render_action('Remove', 'shelf_item_remove', args, 'trash')
        )

    def icon(self, icon_name):
        return '<img class="btn-icon" src="res://Packages/Shelf/assets/img/' + icon_name + '-' + self.color_scheme + '.png">'

    def render_open_file_action(self, path, text, clss):
        return self.render_link('Open ' + path, 'open_file', {'file': path, 'content': 'Could not open ' + path}, text, clss)

    def render_move_action(self, key, args, is_enabled):
        title = ('Move ' + key) if is_enabled else ''
        href = ('shelf_item_move_' + key) if is_enabled else ''
        text = self.icon('arrow-' + key) if is_enabled else '&nbsp;'
        clss = self.action_clss if is_enabled else self.disabled_clss

        return self.render_link(title, href, args, text, clss)

    def render_action(self, title, href, args, icon):
        return self.render_link(title, href, args, self.icon(icon), self.action_clss)

    def render_link(self, title, href, args, text, clss=''):
        href = 'subl:' + sublime.html_format_command(href, args)
        clss = (' class="' + clss + '"') if clss else ''
        return '<a href="' + href + '"' + clss + ' title="' + title + '">' + text + '</a>'
