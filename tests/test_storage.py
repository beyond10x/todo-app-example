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

    def test_save_then_load(self):
        items = [{"text": "buy milk", "done": False}, {"text": "café", "done": True}]
        storage.save(self.file, items)
        self.assertEqual(storage.load(self.file), items)

    def test_save_writes_the_same_bytes_as_before(self):
        storage.save(self.file, [{"text": "café", "done": False}])
        self.assertEqual(
            Path(self.file).read_text(encoding="utf-8"),
            '[\n  {\n    "text": "caf\\u00e9",\n    "done": false\n  }\n]\n',
        )

    def test_save_leaves_no_other_file(self):
        storage.save(self.file, [{"text": "buy milk", "done": False}])
        storage.save(self.file, [{"text": "call home", "done": False}])
        self.assertEqual(os.listdir(self.dir.name), ["todo.json"])

    def test_save_keeps_the_file_permissions(self):
        storage.save(self.file, [])
        os.chmod(self.file, 0o640)
        storage.save(self.file, [{"text": "buy milk", "done": False}])
        self.assertEqual(os.stat(self.file).st_mode & 0o777, 0o640)


if __name__ == "__main__":
    unittest.main()
