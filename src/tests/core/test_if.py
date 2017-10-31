from ancypatch.core.patcher import Patcher
from tests.core.patch import patch_run
import os
import unittest

class TestIf(unittest.TestCase):

    def test_if_hook(self):
        """tests test_if binary hook with pie
        """
        binary_path = os.path.abspath('tests/binary/test_if/test64')
        script_path = os.path.abspath('tests/binary/test_if/test64_hook.py')
        res, out_path = patch_run(binary_path, script_path)
        try:
            self.assertEqual(res, 'hello\n')
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(out_path)

if __name__ == '__main__':
    unittest.main()
