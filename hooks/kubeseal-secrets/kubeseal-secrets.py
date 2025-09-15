#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
import re

KIND_SECRET_RE = re.compile(r'^\s*kind:\s*Secret\s*$', flags=re.I | re.M)
KIND_SEALED_RE = re.compile(r'^\s*kind:\s*SealedSecret\s*$', flags=re.I | re.M)

def seal_secrets(files, controller_name, controller_namespace):
    failures = 0
    for file_path in files:
        file = Path(file_path)
        print(f"\n--- Processing: {file} ---")
        if not file.exists():
            print(f"Warning: File {file} does not exist, skipping")
            continue

        if ".sealed." in file.name:
            print(f"File is already sealed (name contains .sealed.): {file}, skipping")
            continue

        try:
            content = file.read_text()
        except Exception as e:
            print(f"❌ Cannot read {file}: {e}")
            failures += 1
            continue

        if KIND_SEALED_RE.search(content):
            print(f"File already contains a SealedSecret resource, skipping: {file}")
            continue

        if not KIND_SECRET_RE.search(content):
            print(f"No 'kind: Secret' found in {file}. Skipping (not a Secret).")
            continue

        kubeseal_cmd = [
            "kubeseal",
            "--format", "yaml",
            "--controller-name", controller_name,
            "--controller-namespace", controller_namespace,
        ]

        sealed_file = file.with_name(f"{file.stem}.sealed{file.suffix}")

        try:
            proc = subprocess.run(
                kubeseal_cmd,
                input=content.encode(),
                capture_output=True,
                check=True,
            )
            sealed_file.write_bytes(proc.stdout)
            print(f"✅ Sealed secret created: {sealed_file}")
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode(errors="replace") if e.stderr else str(e)
            print(f"❌ Error sealing {file}: {stderr}")
            failures += 1
        except Exception as e:
            print(f"❌ Unexpected error sealing {file}: {e}")
            failures += 1

    if failures:
        print(f"\nFinished with {failures} failure(s).")
        sys.exit(1)
    else:
        print("\nAll done: no failures.")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seal Kubernetes secrets using kubeseal")
    parser.add_argument("--controller-name", required=True, help="Name of the sealed secrets controller")
    parser.add_argument("--controller-namespace", required=True, help="Namespace of the sealed secrets controller")
    parser.add_argument("files", nargs="+", help="Secret files to process")
    args = parser.parse_args()
    seal_secrets(args.files, args.controller_name, args.controller_namespace)
