import tempfile
import unittest
from pathlib import Path

from roomLayout import readLayouts


class RoomLayoutTests(unittest.TestCase):
    def test_empty_csv_rows_separate_layouts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rooms.csv"
            path.write_text("1,2\n3,4\n, \n5,6\n7,8\n", encoding="utf-8")

            self.assertEqual(
                readLayouts(path),
                [
                    [[1, 2], [3, 4]],
                    [[5, 6], [7, 8]],
                ],
            )


if __name__ == "__main__":
    unittest.main()
