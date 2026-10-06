# Notas sobre o build de um Dev Container

[English (UK)](0008-notes-dev-container-build.md)

Para construir a imagem Docker sem abrir o VS Code dentro do contêiner, use a CLI oficial dos Dev Containers (`@devcontainers/cli`).

## 1. Instalação da CLI oficial

Para executar os comandos no terminal, instale a ferramenta globalmente via Node.js:

```bash
npm install -g @devcontainers/cli
```

## 2. Executar apenas o build

Abra o terminal na raiz do projeto (onde está localizado o diretório `.devcontainer`) e execute:

```bash
devcontainer build --workspace-folder .
```

O comando lê `devcontainer.json`, baixa as dependências e constrói a imagem de forma isolada.

A vantagem é verificar se a imagem apresenta erros de sintaxe ou de download antes de tentar entrar no contêiner.

## 3. Alternativa rápida: usar o Docker diretamente

Se o `devcontainer.json` apontar para um Dockerfile local, é possível construir a imagem diretamente com o Docker:

```bash
docker build -t meu-devcontainer .devcontainer/
```
