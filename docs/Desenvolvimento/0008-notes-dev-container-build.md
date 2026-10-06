# Notes about Building a Dev Container

[Português (Brasil)](0008-notas-build-dev-container-pt-br.md)

To build the Docker image without opening VS Code inside the container, use the official Dev Containers CLI (`@devcontainers/cli`).

## 1. Installing the Official CLI

Install the tool globally via Node.js to run its commands from your terminal:

```bash
npm install -g @devcontainers/cli
```

## 2. Building Only

Open a terminal at the root of your project (where the `.devcontainer` directory is located) and run:

```bash
devcontainer build --workspace-folder .
```

This reads `devcontainer.json`, downloads dependencies and builds the image in isolation.

The benefit is that it verifies the image for syntax or download errors before you try to enter the container.

## 3. Quick Alternative: Using Docker Directly

If your `devcontainer.json` points to a local Dockerfile, you can build the image directly with Docker:

```bash
docker build -t meu-devcontainer .devcontainer/
```
