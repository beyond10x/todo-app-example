import os
import tempfile
import unittest
from pathlib import Path

import storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = str(Path(self.dir.name) / "todo.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_load_of_a_missing_file_is_an_empty_list(self):
        self.assertEqual(storage.load(self.file), [])

    def test_save_then_load_round_trip(self):
        items = [{"text": "buy milk", "done": False}, {"text": "café ✓", "done": True}]
        storage.save(self.file, items)
        self.assertEqual(storage.load(self.file), items)

    def test_save_writes_two_space_indent_and_one_newline(self):
        storage.save(self.file, [{"text": "a", "done": False}])
        self.assertEqual(
            Path(self.file).read_text(encoding="utf-8"),
            '[\n  {\n    "text": "a",\n    "done": false\n  }\n]\n',
        )

    def test_save_leaves_no_other_file_in_the_directory(self):
        storage.save(self.file, [{"text": "one", "done": False}])
        storage.save(self.file, [{"text": "two", "done": True}])
        self.assertEqual(os.listdir(self.dir.name), ["todo.json"])

    def test_save_keeps_the_file_permissions(self):
        storage.save(self.file, [])
        os.chmod(self.file, 0o600)
        storage.save(self.file, [{"text": "x", "done": False}])
        self.assertEqual(os.stat(self.file).st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
