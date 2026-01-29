{
  "name": "MLE DevOps Environment",
  "image": "mcr.microsoft.com/devcontainers/python:3.9",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "enableNonRootDocker": "true",
      "moby": "true"
    },
    "ghcr.io/devcontainers/features/python:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-azuretools.vscode-docker",
        "njpwerner.autodocstring"
      ]
    }
  },
  "postCreateCommand": "pip install --upgrade pip"
}