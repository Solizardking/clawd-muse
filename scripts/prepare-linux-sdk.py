#!/usr/bin/env python3
"""Copy and extend upstream Muse SDK without modifying the reference checkout."""
import argparse
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'linux'))
from clawd_muse.service import SPECS

parser = argparse.ArgumentParser()
parser.add_argument('--source', default='/Users/8bit/Untitled/linux')
parser.add_argument('--output', default='build/muse-linux')
args = parser.parse_args()
source, output = Path(args.source).resolve(), Path(args.output).resolve()
if output.exists():
    parser.exit(1, 'Output exists; choose a fresh build directory.\n')
shutil.copytree(source, output, ignore=shutil.ignore_patterns('.venv', '__pycache__', '*.egg-info'))
file = output / 'src/musegadget/executor.py'
text = file.read_text()
anchor = '    def run(self, command: str, params: dict, timeout_ms: int | None = None) -> dict:\n'
if text.count(anchor) != 1:
    parser.exit(1, 'Upstream executor changed; review integration before continuing.\n')
specs = {key: {'description': desc, 'required': {k: {'type': v, 'description': k} for k, v in fields.items()}, 'optional': {}, 'timeout_ms': 30000} for key, (desc, fields) in SPECS.items()}
for key in ('clawd.voice', 'clawd.muse', 'clawd.muse.tokens'):
    specs[key]['optional']['protocol'] = {'type': 'string', 'description': 'responses, chat/completions, or messages'}
    specs[key]['timeout_ms'] = 190000
specs['clawd.voice']['optional']['model'] = {'type': 'string', 'description': 'Muse Spark model ID'}
registration = '\nCOMMAND_SPECS.update(' + repr(specs) + ')\n\n'
text = text.replace('class Executor:\n', registration + 'class Executor:\n')
handler = '''        if command.startswith("clawd."):
            import shlex
            # The SDK child options enforce its configured unprivileged run-as user.
            line = shlex.join([sys.executable, "-m", "clawd_muse.service", command, json.dumps(params)])
            return self.system_run({"command": line}, timeout_ms)
'''
text = text.replace(anchor, anchor + handler)
file.write_text(text)
print(f'Prepared {output}. Install the companion in the same Python environment as this SDK.')
