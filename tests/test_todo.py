import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import todo


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = str(Path(self.dir.name) / "todo.json")

    def tearDown(self):
        self.dir.cleanup()

    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = todo.main(["--file", self.file, *args])
        return code, out.getvalue()

    def test_a_missing_file_is_an_empty_list(self):
        self.assertEqual(todo.load(self.file), [])

    def test_an_empty_file_is_an_empty_list(self):
        Path(self.file).write_text("", encoding="utf-8")
        self.assertEqual(self.run_cli("list"), (0, ""))
        self.assertEqual(self.run_cli("add", "buy milk")[0], 0)
        self.assertEqual(self.run_cli("list"), (0, "1. [ ] buy milk\n"))

    def test_a_file_of_white_space_is_an_empty_list(self):
        Path(self.file).write_text(" \n\t\n", encoding="utf-8")
        self.assertEqual(self.run_cli("list"), (0, ""))
        self.assertEqual(self.run_cli("add", "buy milk")[0], 0)
        self.assertEqual(self.run_cli("list"), (0, "1. [ ] buy milk\n"))

    def assert_refused(self, content):
        Path(self.file).write_text(content, encoding="utf-8")
        for args in (["list"], ["add", "buy milk"], ["done", "1"], ["remove", "1"]):
            err = io.StringIO()
            with redirect_stderr(err):
                code, out = self.run_cli(*args)
            self.assertEqual((code, out), (1, ""), args)
            self.assertEqual(err.getvalue(), f"todo: {self.file} is not a todo list\n", args)
            self.assertEqual(Path(self.file).read_text(encoding="utf-8"), content, args)

    def test_a_file_that_is_not_json_is_refused(self):
        self.assert_refused("buy milk\n")

    def test_a_file_holding_a_json_object_is_refused(self):
        self.assert_refused('{"text": "buy milk", "done": false}\n')

    def test_add_then_list(self):
        self.assertEqual(self.run_cli("add", "buy milk")[0], 0)
        self.assertEqual(self.run_cli("add", "call home")[0], 0)
        self.assertEqual(
            self.run_cli("list"), (0, "1. [ ] buy milk\n2. [ ] call home\n")
        )

    def test_done_marks_one_item(self):
        self.run_cli("add", "buy milk")
        self.run_cli("add", "call home")
        self.assertEqual(self.run_cli("done", "2")[0], 0)
        self.assertEqual(
            self.run_cli("list"), (0, "1. [ ] buy milk\n2. [x] call home\n")
        )

    def test_done_refuses_a_number_out_of_range(self):
        self.run_cli("add", "buy milk")
        self.assertEqual(self.run_cli("done", "2")[0], 1)
        self.assertEqual(self.run_cli("done", "0")[0], 1)

    def test_remove_moves_later_items_up(self):
        self.run_cli("add", "buy milk")
        self.run_cli("add", "call home")
        self.run_cli("add", "water plants")
        self.assertEqual(self.run_cli("remove", "2")[0], 0)
        self.assertEqual(
            self.run_cli("list"), (0, "1. [ ] buy milk\n2. [ ] water plants\n")
        )

    def test_remove_refuses_a_number_out_of_range(self):
        self.run_cli("add", "buy milk")
        self.run_cli("add", "call home")
        self.run_cli("add", "water plants")
        before = Path(self.file).read_text(encoding="utf-8")
        self.assertEqual(self.run_cli("remove", "0")[0], 1)
        self.assertEqual(self.run_cli("remove", "4")[0], 1)
        self.assertEqual(Path(self.file).read_text(encoding="utf-8"), before)

    def test_add_refuses_empty_text(self):
        with self.assertRaises(ValueError):
            todo.add([], "   ")


if __name__ == "__main__":
    unittest.main()
