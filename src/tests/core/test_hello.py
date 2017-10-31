from ancypatch.core.patcher import Patcher
from tests.core.patch import patch_run
import unittest
import os

class TestHello(unittest.TestCase):

    def test_hello_hook_nopie(self):
        """tests hello binary hook with no pie
        """
        binary_path = os.path.abspath('tests/binary/test_hello/test64_nopie') 
        script_path = os.path.abspath('tests/binary/test_hello/test64_nopie_hook.py') 
        res, out_path = patch_run(binary_path, script_path)
        try:
            self.assertEqual(res, 'world\n')
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(out_path)

    def test_hello_hook(self):
        """tests hello binary hook with pie
        """
        binary_path = os.path.abspath('tests/binary/test_hello/test64')
        script_path = os.path.abspath('tests/binary/test_hello/test64_hook.py')
        res, out_path = patch_run(binary_path, script_path)
        try:
            self.assertEqual(res, 'world\n')
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(out_path)

    def test_hello_patch_nopie(self):
        """tests 64 bits no pie binary patch
        """
        binary_path = os.path.abspath('tests/binary/test_hello/test64_nopie')
        script_path = os.path.abspath('tests/binary/test_hello/test64_nopie_patch.py')
        res, out_path = patch_run(binary_path, script_path)
        try:
            self.assertEqual(res, 'patched\n')
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(out_path)

    def test_hello_patch(self):
        """tests 64 bits with pie binary
        """
        binary_path = os.path.abspath('tests/binary/test_hello/test64')
        script_path = os.path.abspath('tests/binary/test_hello/test64_patch.py')
        res, out_path = patch_run(binary_path, script_path)
        try:
            self.assertEqual(res, 'patched\n')
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(out_path)
        

if __name__ == '__main__':
    unittest.main()
