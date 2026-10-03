#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    binary=Path(directory)/'pocket-test'
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',
                    '-I'+str(root/'components/pocket_wallet'),str(root/'components/pocket_wallet/pocket_wallet.c'),
                    str(root/'tests/state_test.c'),'-o',str(binary)],check=True)
    subprocess.run([str(binary)],check=True)
print('Firmware state checks passed (expiry, physical edge, replay, cancellation, bounds).')
