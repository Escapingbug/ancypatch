import os
from ancypatch.core.patcher import Patcher

def patch_run(binary, script):
    """for test, patch a binary with script and run
    Args:
      binary (str): binary path
      script (str): patch script path
    Returns:
      (str, str): a tuple of (output_str, output_path), where output_str is the output of the 
                  patched binary, and output_path is the temp file patched
    """
    patcher = Patcher(binary)
    patcher.add(script)
    patcher.patch()
    out_path = './test_patched'
    patcher.save(out_path)
    res = os.popen(out_path).read()
    return res, out_path
