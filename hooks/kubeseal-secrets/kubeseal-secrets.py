#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

def seal_secrets(files, controller_name, controller_namespace):
    for file_path in files:
        file = Path(file_path)
        if not file.exists():
            print(f"Warning: File {file} does not exist, skipping")
            continue
            
        sealed_file = file.with_suffix(file.suffix + ".sealed.yaml")
        if sealed_file.exists():
            print(f"Sealed file already exists: {sealed_file}, skipping")
            continue

        kubeseal_cmd = [
            "kubeseal",
            "--format", "yaml",
            "--controller-name", controller_name,
            "--controller-namespace", controller_namespace,
        ]

        try:
            with Path(file).open("rb") as f:
                result = subprocess.run(
                    kubeseal_cmd,
                    input=f.read(),
                    capture_output=True,
                    check=True,
                    text=False,
                )
            sealed_file.write_bytes(result.stdout)
            print(f"✅ Sealed secret created: {sealed_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error sealing {file}: {e.stderr.decode()}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seal Kubernetes secrets using kubeseal")
    parser.add_argument("--controller-name", required=True, help="Name of the sealed secrets controller")
    parser.add_argument("--controller-namespace", required=True, help="Namespace of the sealed secrets controller")
    parser.add_argument("files", nargs="+", help="Secret files to process")
    
    args = parser.parse_args()
    seal_secrets(args.files, args.controller_name, args.controller_namespace)
