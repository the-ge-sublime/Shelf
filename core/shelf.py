# File name: shelf.py
# Created:   2024-03-11 09:24
# @author    Gabriel Tenita <g1704578400@tenita.eu@tenita.eu>
# @see       https://github.com/the-ge/
# @copyright Copyright (c) 2026-present Gabriel Tenita
# @license   https://www.apache.org/licenses/LICENSE-2.0 Apache License version 2.0

from __future__ import annotations

import csv
import logging
from pathlib import Path

import sublime

logging.basicConfig(level='DEBUG', format='%(levelname)s: %(message)s')  # DEBUG INFO WARNING ERROR CRITICAL
logger = logging.getLogger(__name__)


class Shelf:
    key = None

    def __init__(self, file: Path) -> None:
        self.file = file

    def clear(self) -> None:
        if self.file:
            with self.file.open("w", encoding="utf_8"):
                pass

    def has_file(self) -> str:
        return self.file.exists()

    def read_inventory(self) -> list[tuple]:
        if not self.has_file():
            return []

        with self.file.open(encoding="utf_8", newline="") as f:
            return [tuple(row) for row in csv.reader(f)]

    def write(self, items: list) -> None:
        if not self.has_file():
            logger.info('Creating %s...', self.file)

        with self.file.open("w", encoding="utf_8", newline="") as f:
            csv.writer(f).writerows(items)

    def add(self, path: str) -> None:
        item = (Path(path).name, path)
        items = self.read_inventory()

        if item in items:
            logger.info('Item already on the %s shelf.', self.key)
            return

        items.append(item)
        self.write(items)
        logger.info('Added %s to the %s shelf.', item[0], self.key)

    def move_up(self, item: tuple[str, str]) -> None:
        items = self.read_inventory()

        try:
            index = items.index(item)
        except ValueError:
            return

        if index == 0:
            return

        items[index - 1], items[index] = items[index], items[index - 1]
        self.write(items)

    def move_down(self, item: tuple[str, str]) -> None:
        items = self.read_inventory()

        try:
            index = items.index(item)
        except ValueError:
            return

        if index >= len(items) - 1:
            return

        items[index], items[index + 1] = items[index + 1], items[index]
        self.write(items)

    def remove(self, item: tuple[str, str]) -> None:
        items = self.read_inventory()

        try:
            items.remove(item)
        except ValueError:
            return

        self.write(items)
        logger.info('Removed %s from the %s shelf.', item[0], self.key)


class CommonShelf(Shelf):
    key = "common"

    def __init__(self) -> None:
        super().__init__(Path(sublime.packages_path()) / 'User' / 'Default.shelf')


class ProjectShelf(Shelf):
    key = "project"

    def __init__(self) -> None:
        project_filename = Path(sublime.active_window().project_file_name())
        shelf_filename = project_filename.with_suffix('.shelf')
        super().__init__(shelf_filename)
