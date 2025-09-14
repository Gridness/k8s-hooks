#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def seal_secrets(pattern="*secret*"):
    secrets = list(Path(".").rglob(pattern))
    for file in secrets:
        sealed_file = file.with_suffix(file.suffix + ".sealed.yaml")
        if not sealed_file.exists():
            with open(file, "rb") as f:
                result = subprocess.run(
                    ["kubeseal", "--format", "yaml"],
                    input=f.read(),
                    capture_output=True,
                    check=True
                )
            sealed_file.write_bytes(result.stdout)
            print(f"Sealed secret created: {sealed_file}")

if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else "*secret*"
    seal_secrets(pattern)
