# Build de Dev Container

Para fazer apenas o build (construir a imagem Docker) sem abrir o VS Code dentro do contêiner, você pode usar a ferramenta oficial de CLI dos Dev Containers (@devcontainers/cli).

## Como instalar a CLI oficial

Para rodar os comandos no seu terminal, instale a ferramenta globalmente via Node.js:

```bash
npm install -g @devcontainers/cli
```

## Comando para fazer apenas o build

Abra o terminal na raiz do seu projeto (onde a pasta .devcontainer está localizada) e execute:

```bash
devcontainer build --workspace-folder .
```

O que ele faz:
- Lê o arquivo devcontainer.json, baixa as dependências e constrói a imagem Docker de forma isolada.

Vantagem:
- Garante que a imagem está sem erros de sintaxe ou de download antes de você tentar entrar nela.

## Alternativa rápida: Usando o próprio Docker

Se o seu devcontainer.json aponta para um Dockerfile local, você pode ir direto na fonte e buildar a imagem usando o Docker tradicional:

```bash
docker build -t meu-devcontainer .devcontainer/
```