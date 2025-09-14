# Kubernetes Hooks
This repository contains reusable Kubernetes-related Git hooks that simplify management of k8s resources manifests. Particularly useful for any gitops repositories

# Available Hooks
## Kubeseal Secrets Hook
This pre-commit hook scans your Git repository for secret files matching a configurable pattern and creates sealed secrets using `kubeseal`. It ensures that all secrets are encrypted before being committed, enhancing security and compliance.

You can specify regex pattern by which the script will look for secrets files in your repo directory in the hook `args` section of your pre-commit config

# Usage
Integrate the Kubeseal Hook in Your Project

1. Add the following configuration to your project’s `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/Gridness/k8s-hooks
    rev: main  # or a specific tag/commit
    hooks:
      - id: kubeseal-secrets # or any other script you wanna run
        name: Kubeseal secrets files
        entry: ./kubeseal-secrets.sh # scecify script name
        language: script
        args: # Specify args for the hook
          - '*secret*'
        types: [file]
```
2. Install pre-commit hooks:
```bash
pre-commit install
```
3. On each commit, the hook will seal any unsealed secrets matching the specified pattern.

# Requirements
- [kubeseal](https://github.com/bitnami-labs/sealed-secrets) CLI must be installed and available in your PATH
- [pre-commit](https://pre-commit.com/) framework installed in your local environment

# Contributing
Contributions to add new hooks, improve existing ones, or fix issues are welcome! Please open issues or pull requests.

# License
This repository is licensed under the MIT License
