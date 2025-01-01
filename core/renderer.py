# -*- coding: UTF-8 -*-
# https://www.sublimetext.com/docs/minihtml.html

import sublime
import os
from Shelf.core.shelf import CommonShelf, ProjectShelf


class Renderer:
    def render_shelves(self, color_scheme):
        self.color_scheme = color_scheme

        prject_shelf, prject_max_name = self.render_shelf(ProjectShelf())
        common_shelf, common_max_name = self.render_shelf(CommonShelf())
        # make up for the lack of table support in minihtml
        # by calculating the file names column length using a totally magic factor of 0.6
        # it will probably fail with wider character fonts
        name_rems = round(max(len(prject_max_name), len(common_max_name)) * 0.6)
        css = (
            '<style>\n'
            + sublime.load_resource('Packages/Shelf/assets/css/shelf.css').strip()
            + '\n'
            + '  .main {\n'
            + '    width: '
            + str(name_rems)
            + 'rem;\n'
            + '  }\n'
            + '</style>\n'
        )

        return (
            '\n'
            + '<body id="shelf-popup">\n'
            + css
            + '    <div class="close">\n'
            + '        <a href="#" class="close-btn btn"><img class="btn-icon" src="res://Packages/Shelf/assets/img/close-'
            + self.color_scheme
            + '.png"></a>'
            + '    </div>\n'
            + '    <h3 class="header">\n'
            + '        <span>PROJECT</span>\n'
            + '    </h3>\n'
            + '    <div class="table">\n'
            + prject_shelf
            + '    </div>\n'
            + '    <h3 class="header">COMMON</h3>\n'
            + '    <div class="table">\n'
            + common_shelf
            + '    </div>\n'
            + '    </body>'
        )

    def render_shelf(self, shelf):
        items = shelf.read()
        rendered, max_name, is_odd, k, count = '', '', False, 0, len(items)
        while k < count:
            name, path = item = items[k]
            alt_class = 'tr-' + ('odd' if is_odd else 'even')
            open_file_action = self.render_action(
                name='open_file',
                args={'file': path, 'content': 'Could not open ' + path},
                text=name,
                clss='btn text-btn',
                title='Open ' + path,
            )
            rendered += (
                '        <div class="tr ' + alt_class + ' tbody">\n'
                + '            <h4 class="td main">' + open_file_action + '</h4>\n'
                + '            <div class="td aside">' + self.side_actions(item, shelf.key) + '</div>\n'
                + '        </div>\n'
            )
            max_name = max_name if max(len(max_name), len(name)) == len(max_name) else name
            is_odd = not is_odd
            k += 1

        return rendered, max_name

    def side_actions(self, item, shelf):
        args = {'item': item, 'shelf': shelf}
        clss = 'btn action-btn'
        _, path = item
        containing_folder_path = os.path.dirname(path)
        side_actions = self.render_action(
            'open_dir',
            {'dir': containing_folder_path},
            self.icon('folder'),
            clss,
            'Open containing folder (' + containing_folder_path + ')',
        )
        actions = [
            ('shelf_item_move_up', self.icon('arrow-up'), 'Move up'),
            ('shelf_item_move_down', self.icon('arrow-down'), 'Move down'),
            ('shelf_item_remove', self.icon('trash'), 'Remove'),
        ]

        return side_actions + ''.join([self.render_action(name, args, text, clss, title) for (name, text, title) in actions])

    def icon(self, icon_name):
        return '<img class="btn-icon" src="res://Packages/Shelf/assets/img/' + icon_name + '-' + self.color_scheme + '.png">'

    def render_action(self, name, args, text, clss, title):
        href = 'subl:' + sublime.html_format_command(name, args)
        return '<a href="' + href + '" class="' + clss + '" title="' + title + '">' + text + '</a>'
