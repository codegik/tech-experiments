import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE = """# T

<!-- techs:start -->
## Databases

| Tech | What it is | Added |
|---|---|---|
| [Postgres](https://www.postgresql.org) | Relational database | 2026-01-01 |
<!-- techs:end -->

footer
"""


class TechsScript(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        self.file = Path(path)
        self.file.write_text(BASE)
        self.addCleanup(self.file.unlink)

    def run_cmd(self, *args):
        env = {**os.environ, "TECHS_FILE": str(self.file)}
        return subprocess.run([str(ROOT / "techs.sh"), *args], env=env,
                              capture_output=True, text=True)

    def add(self, name, url, category, desc="Something"):
        return self.run_cmd("add", "--name", name, "--url", url,
                            "--category", category, "--desc", desc, "--date", "2026-10-24")

    def test_real_readme_is_valid(self):
        r = subprocess.run([str(ROOT / "techs.sh"), "check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_add_sorts_categories_and_rows_and_keeps_surroundings(self):
        self.assertEqual(self.add("Redis", "https://redis.io", "Databases").returncode, 0)
        self.assertEqual(self.add("cua", "https://cua.ai", "AI Agents").returncode, 0)
        self.assertEqual(self.add("MySQL", "https://www.mysql.com", "databases").returncode, 0)
        text = self.file.read_text()
        self.assertTrue(text.startswith("# T\n\n"))
        self.assertTrue(text.endswith("<!-- techs:end -->\n\nfooter\n"))
        self.assertLess(text.index("## AI Agents"), text.index("## Databases"))
        self.assertLess(text.index("[MySQL]"), text.index("[Postgres]"))
        self.assertLess(text.index("[Postgres]"), text.index("[Redis]"))
        self.assertEqual(text.count("## Databases"), 1)
        self.assertEqual(self.run_cmd("check").returncode, 0)

    def test_add_rejects_duplicate_name_or_url(self):
        r = self.add("postgres", "https://example.com", "Other")
        self.assertEqual(r.returncode, 3)
        r = self.add("PG", "https://www.postgresql.org/", "Other")
        self.assertEqual(r.returncode, 3)
        self.assertEqual(self.file.read_text(), BASE)

    def test_add_rejects_pipe_and_bad_url(self):
        self.assertEqual(self.add("X", "https://x.dev", "Y", desc="a | b").returncode, 1)
        self.assertEqual(self.add("X", "x.dev", "Y").returncode, 1)
        self.assertEqual(self.file.read_text(), BASE)

    def test_check_catches_hand_edit_mistakes(self):
        self.file.write_text(BASE.replace(
            "| [Postgres]", "| [Redis](https://redis.io) | Cache | 2026-01-01 |\n| [Postgres]"))
        r = self.run_cmd("check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("alphabetical", r.stderr)
        self.file.write_text(BASE.replace("| 2026-01-01 |", "|"))
        self.assertEqual(self.run_cmd("check").returncode, 1)


if __name__ == "__main__":
    unittest.main()
