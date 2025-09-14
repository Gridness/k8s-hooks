#!/bin/bash

set -e

pattern="${1:-*secret*}"

secrets=$(find . -type f -name "$pattern")
for file in $secrets; do
    sealed_file=${file}.sealed.yaml
    if [ ! -f $sealed_file ]; then
        kubeseal --format yaml < "$file" > "$sealed_file"
        echo "Sealed secret created: $sealed_file"
    fi
done
