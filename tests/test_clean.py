import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import clean


class Engine(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.root = self.base / "pip" / "wheels"
        self.bucket = self.root / "ab" / "cd" / "ef" / ("0" * 50)
        self.bucket.mkdir(parents=True)
        self.wheel = self.bucket / "private_package-1.0-py3-none-any.whl"
        self.old(self.wheel)

    def old(self, path):
        path.write_bytes(b"cached wheel fixture")
        age = time.time() - 40 * 86400
        os.utime(path, (age, age))

    def invoke(self, *args, confirm="OUI", tty=True, admin=False):
        output = io.StringIO()
        with (patch.object(clean, "cache_root", return_value=self.root),
              patch.object(clean, "elevated", return_value=admin),
              patch.object(sys.stdin, "isatty", return_value=tty),
              patch("builtins.input", side_effect=(confirm if callable(confirm) else lambda _: confirm)),
              contextlib.redirect_stdout(output), contextlib.redirect_stderr(output)):
            code = clean.main(args)
        return code, output.getvalue()

    def test_audit_share(self):
        before = self.wheel.stat()
        code, output = self.invoke("--share")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), dict(candidats=1, octets=before.st_size, anomalies=0))
        self.assertEqual(self.wheel.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertNotIn(self.wheel.name, self.invoke()[1])
        self.assertIn(self.wheel.name, self.invoke("--detail")[1])

    def test_only_the_reviewed_wheel(self):
        fresh = self.bucket / "new-1-py3-none-any.whl"
        fresh.touch()
        unrelated = self.bucket / "notes.txt"
        self.old(unrelated)
        stray = self.root / self.wheel.name
        self.old(stray)
        sibling = self.base / self.wheel.name
        self.old(sibling)
        self.assertEqual(self.invoke("--clean")[0], 0)
        self.assertFalse(self.wheel.exists())
        self.assertTrue(all(p.exists() for p in (fresh, unrelated, stray, sibling, self.bucket)))
        self.assertEqual(self.invoke("--clean")[0], 0)

    def test_missing_cache(self):
        self.root = self.base / "absent"
        self.assertEqual(json.loads(self.invoke("--share")[1])["candidats"], 0)
        self.assertFalse(self.root.exists())

    def test_confirmation_gates(self):
        for kwargs, code in [({"confirm": "oui"}, 0), ({"tty": False}, 1), ({"admin": True}, 1)]:
            with self.subTest(kwargs=kwargs):
                self.assertEqual(self.invoke("--clean", **kwargs)[0], code)
                self.assertTrue(self.wheel.exists())

    def test_changed_since_preview(self):
        def replace(_):
            self.wheel.write_bytes(b"other data")
            return "OUI"
        self.assertEqual(self.invoke("--clean", confirm=replace)[0], 1)
        self.assertEqual(self.wheel.read_bytes(), b"other data")

    def test_new_files_excluded_after_preview(self):
        later = self.bucket / "later-1-py3-none-any.whl"
        def add(_):
            self.old(later)
            return "OUI"
        self.assertEqual(self.invoke("--clean", confirm=add)[0], 0)
        self.assertTrue(later.exists())

    def test_git_ancestor(self):
        (self.base / ".git").touch()
        self.assertEqual(self.invoke("--clean")[0], 1)
        self.assertTrue(self.wheel.exists())

    def test_hard_link(self):
        os.link(self.wheel, self.base / "outside")
        self.assertEqual(json.loads(self.invoke("--share")[1])["candidats"], 0)

    @unittest.skipUnless(sys.platform == "darwin", "macOS")
    def test_macos_file_and_directory_symlinks(self):
        link = self.bucket / "other-1-py3-none-any.whl"
        link.symlink_to(self.wheel)
        (self.root / "aa").symlink_to(self.base, target_is_directory=True)
        self.assertEqual(self.invoke("--clean")[0], 1)
        self.assertTrue(self.wheel.exists())
        (self.root / "aa").unlink()
        self.assertEqual(json.loads(self.invoke("--share")[1])["candidats"], 1)

    @unittest.skipUnless(os.name == "nt", "Windows")
    def test_windows_junction(self):
        target = self.base / "target"
        target.mkdir()
        junction = self.root / "aa"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(target)],
                       capture_output=True, check=True)
        self.addCleanup(os.rmdir, junction)
        self.assertEqual(self.invoke("--clean")[0], 1)
        self.assertTrue(self.wheel.exists())

    @unittest.skipUnless(os.name == "nt", "Windows")
    def test_windows_locked_file(self):
        with self.wheel.open("rb"):
            self.assertEqual(self.invoke("--clean")[0], 1)
        self.assertTrue(self.wheel.exists())

    def test_real_platform_root(self):
        with patch.dict(os.environ, {"PIP_CACHE_DIR": str(self.base), "HOME": str(self.base),
                                     "USERPROFILE": str(self.base)}):
            root = clean.cache_root()
        self.assertNotIn(self.base, root.parents)
        expected = "AppData/Local/pip/Cache/wheels" if os.name == "nt" else "Library/Caches/pip/wheels"
        self.assertTrue(root.as_posix().endswith(expected))

    def test_permission_failure(self):
        with patch.object(Path, "unlink", side_effect=PermissionError):
            self.assertEqual(self.invoke("--clean")[0], 1)
        self.assertTrue(self.wheel.exists())

    def test_no_arbitrary_path_option(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            clean.main(["--root", str(self.base)])

