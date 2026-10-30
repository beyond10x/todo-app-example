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

    def test_priorities_render_and_sort_without_changing_todo_numbers(self):
        self.assertEqual(self.run_cli("add", "buy milk")[0], 0)
        self.assertEqual(self.run_cli("add", "water plants", "--priority", "low")[0], 0)
        self.assertEqual(self.run_cli("add", "call home", "--priority", "high")[0], 0)
        self.assertEqual(self.run_cli("add", "write a card")[0], 0)

        self.assertEqual(
            self.run_cli("list"),
            (0, "1. [ ] buy milk\n2. [ ] (low) water plants\n"
                "3. [ ] (high) call home\n4. [ ] write a card\n"),
        )
        self.assertEqual(
            self.run_cli("list", "--sort", "priority"),
            (0, "3. [ ] (high) call home\n1. [ ] buy milk\n"
                "4. [ ] write a card\n2. [ ] (low) water plants\n"),
        )
        self.assertEqual(self.run_cli("done", "3")[0], 0)
        self.assertEqual(
            self.run_cli("list", "--sort", "priority"),
            (0, "3. [x] (high) call home\n1. [ ] buy milk\n"
                "4. [ ] write a card\n2. [ ] (low) water plants\n"),
        )

    def test_unknown_priority_is_refused_without_changing_the_file(self):
        self.assertEqual(self.run_cli("add", "buy milk")[0], 0)
        before = Path(self.file).read_bytes()
        errors = io.StringIO()
        with redirect_stderr(errors):
            with self.assertRaises(SystemExit) as result:
                todo.main(["--file", self.file, "add", "call home", "--priority", "urgent"])
        self.assertEqual(result.exception.code, 2)
        self.assertEqual(Path(self.file).read_bytes(), before)

    def test_items_without_a_priority_keep_the_legacy_listing(self):
        Path(self.file).write_text(
            '[{"text": "buy milk", "done": false}, '
            '{"text": "water plants", "done": true}]',
            encoding="utf-8",
        )
        self.assertEqual(
            self.run_cli("list"), (0, "1. [ ] buy milk\n2. [x] water plants\n")
        )


if __name__ == "__main__":
    unittest.main()
