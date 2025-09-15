# Kubeseal Secrets Hook
This pre-commit hook scans your Git repository for secret files matching a configurable pattern and creates sealed secrets using `kubeseal`. It ensures that all secrets are encrypted before being committed, enhancing security and compliance.

You can specify regex pattern by which the script will look for secrets files in your repo directory in the hook `args` section of your pre-commit config
# Usage
```yaml
repos:
  - repo: https://github.com/Gridness/k8s-hooks
    rev: 3.0  # or a specific tag/commit
    hooks:
      - id: kubeseal-secrets
        args: # you can ommit these values if you want to use the default ones listed below
          - "--controller-name sealed-secrets"
          - "--controller-namespace sealed-secrets"
        files: ["*secret*.yaml"] # regex pattern of your secrets manifests filenames
```
# Requirements
- [sealed-secrets](https://artifacthub.io/packages/helm/bitnami-labs/sealed-secrets) controller must be deployed in your Kubernetes cluster
- [kubeseal](https://github.com/bitnami-labs/sealed-secrets) CLI must be installed on the machine you are working with secrets and running this hook
