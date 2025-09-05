import sublime
import os
import csv
#from Shelf.core.debug import _d


class Shelf:
    key = None

    def __init__(self, file):
        self.file = file

    def clear(self):
        if self.file:
            with open(self.file, 'w', encoding='utf_8'):
                pass

    def hasFile(self):
        return self.file and os.path.exists(self.file)

    def read(self):
        if not self.hasFile():
            return ()

        with open(self.file, 'r', encoding='utf_8', newline='') as f:
            items = tuple(tuple(row) for row in csv.reader(f))

        return items

    def write(self, items):
        with open(self.file, 'w+', encoding='utf_8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(items)

    def add(self, item):
        name = os.path.basename(item)
        print(f'Adding {name} to {str(self.key)} shelf...')
        new = (name, item)
        items = self.read()

        if new in items:
            print('Item already on the {str(self.key)} shelf')
            return

        items += (new,)
        self.write(items)

    def move_up(self, item):
        items = self.read()
        k = items.index(item)

        if k < 1:
            return

        self.write(items[0:k - 1] + (item,) + (items[k - 1],) + items[k + 1:])

    def move_down(self, item):
        items = self.read()
        k = items.index(item)

        if k > len(items) - 1:
            return

        self.write(items[0:k] + (items[k + 1],) + (item,) + items[k + 2:])

    def remove(self, item):
        print('Removing ' + item[0] + ' from the ' + str(self.key) + ' shelf...')
        items = self.read()
        if item in items:
            k = items.index(item)
            items = items[0:k] + items[k + 1:]
            self.write(items)


class CommonShelf(Shelf):
    key = 'common'

    def __init__(self):
        super().__init__(os.path.join(sublime.packages_path(), 'User', 'shelf-common.csv'))


class ProjectShelf(Shelf):
    key = 'project'
    def __init__(self):
        project = sublime.active_window().project_file_name()
        if project:
            super().__init__(f'{project}.shelf')
