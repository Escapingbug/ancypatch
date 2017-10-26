import ancypatch
import unittest

from ancypatch.core.patcher import Patcher
from ancypatch.core.binary import Binary

class TestPatcher(unittest.TestCase):

    def test_init(self):
        patcher = Patcher('./tests/core/binary')
        self.assertEqual(Binary, type(patcher.bin))

if __name__ == '__main__':
    unittest.main()
