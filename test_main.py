import tempfile
import unittest
from pathlib import Path
from main import build, suspicious


class SqlLabTests(unittest.TestCase):
    def test_groups_failures(self):
        events = [{"timestamp": str(i), "username": f"u{i%2}", "source_ip": "192.0.2.4", "result": "failure", "asset": "vpn"} for i in range(3)]
        with tempfile.TemporaryDirectory() as tmp:
            database = Path(tmp) / "lab.db"
            build(database, events)
            self.assertEqual(suspicious(database)[0]["targeted_users"], 2)


if __name__ == "__main__":
    unittest.main()
