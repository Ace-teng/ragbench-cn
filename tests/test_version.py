import unittest

import ragbench


class VersionTest(unittest.TestCase):
    def test_package_version_matches_release(self) -> None:
        self.assertEqual(ragbench.__version__, "0.2.0")


if __name__ == "__main__":
    unittest.main()
