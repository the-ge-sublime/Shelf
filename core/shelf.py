# -*- coding: UTF-8 -*-

import csv
import os

import sublime


class Shelf:
    key = None

    def __init__(self, file):
        self.file = file

    def clear(self):
        if self.file:
            with open(self.file, "w", encoding="utf_8"):
                pass

    def has_file(self):
        return self.file is not None and os.path.exists(self.file)

    def read(self):
        if not self.has_file():
            return []

        with open(self.file, "r", encoding="utf_8", newline="") as f:
            return [tuple(row) for row in csv.reader(f)]

    def write(self, items):
        if not self.has_file():
            print(f"Creating {self.file}...")

        with open(self.file, "w", encoding="utf_8", newline="") as f:
            csv.writer(f).writerows(items)

    def add(self, path):
        item = (os.path.basename(path), path)
        items = self.read()

        if item in items:
            print(f"Item already on the {self.key} shelf.")
            return

        items.append(item)
        self.write(items)

        print(f"Added {item[0]} to the {self.key} shelf.")

    def move_up(self, item):
        items = self.read()

        try:
            index = items.index(item)
        except ValueError:
            return

        if index == 0:
            return

        items[index - 1], items[index] = items[index], items[index - 1]
        self.write(items)

    def move_down(self, item):
        items = self.read()

        try:
            index = items.index(item)
        except ValueError:
            return

        if index >= len(items) - 1:
            return

        items[index], items[index + 1] = items[index + 1], items[index]
        self.write(items)

    def remove(self, item):
        items = self.read()

        try:
            items.remove(item)
        except ValueError:
            return

        self.write(items)

        print(f"Removed {item[0]} from the {self.key} shelf.")


class CommonShelf(Shelf):
    key = "common"

    def __init__(self):
        super().__init__(
            os.path.join(
                sublime.packages_path(),
                "User",
                "shelf-common.csv",
            )
        )


class ProjectShelf(Shelf):
    key = "project"

    def __init__(self):
        project = sublime.active_window().project_file_name()
        if project:
            super().__init__(f"{project}.shelf")
