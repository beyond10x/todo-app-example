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

    def add_one_of_each_priority(self):
        self.run_cli("add", "water plants", "--priority", "low")
        self.run_cli("add", "call home")
        self.run_cli("add", "buy milk", "--priority", "high")
        self.run_cli("add", "pay rent", "--priority", "normal")
        self.run_cli("add", "fix bike", "--priority", "high")

    def test_list_shows_a_priority_that_is_not_normal(self):
        self.add_one_of_each_priority()
        self.assertEqual(
            self.run_cli("list"),
            (
                0,
                "1. [ ] (low) water plants\n2. [ ] call home\n3. [ ] (high) buy milk\n"
                "4. [ ] pay rent\n5. [ ] (high) fix bike\n",
            ),
        )

    def test_list_sorted_by_priority_keeps_each_todos_number(self):
        self.add_one_of_each_priority()
        self.assertEqual(
            self.run_cli("list", "--sort", "priority"),
            (
                0,
                "3. [ ] (high) buy milk\n5. [ ] (high) fix bike\n2. [ ] call home\n"
                "4. [ ] pay rent\n1. [ ] (low) water plants\n",
            ),
        )

    def test_done_acts_on_the_number_the_sorted_list_shows(self):
        self.add_one_of_each_priority()
        first_sorted = self.run_cli("list", "--sort", "priority")[1].splitlines()[0]
        number = first_sorted.split(".")[0]
        self.assertEqual(self.run_cli("done", number)[0], 0)
        self.assertEqual(
            self.run_cli("list", "--sort", "priority")[1].splitlines()[0],
            "3. [x] (high) buy milk",
        )

    def test_add_refuses_an_unknown_priority(self):
        self.run_cli("add", "buy milk")
        before = Path(self.file).read_text(encoding="utf-8")
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            self.run_cli("add", "call home", "--priority", "urgent")
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(Path(self.file).read_text(encoding="utf-8"), before)

    def test_a_file_without_priorities_lists_as_before(self):
        Path(self.file).write_text(
            '[{"text": "buy milk", "done": false}, {"text": "call home", "done": true}]\n',
            encoding="utf-8",
        )
        self.assertEqual(
            self.run_cli("list"), (0, "1. [ ] buy milk\n2. [x] call home\n")
        )
        self.assertEqual(
            self.run_cli("list", "--sort", "priority"),
            (0, "1. [ ] buy milk\n2. [x] call home\n"),
        )


if __name__ == "__main__":
    unittest.main()
