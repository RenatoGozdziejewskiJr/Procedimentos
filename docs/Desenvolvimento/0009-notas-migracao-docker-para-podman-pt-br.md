# Notas sobre a migração do Docker Desktop para Podman

[English (UK)](0009-notes-docker-to-podman-migration.md)

Este guia documenta o passo a passo para substituir o Docker Desktop pelo Podman Desktop no Windows, mantendo compatibilidade total com o uso de Dev Containers no VS Code por meio do WSL 2.

## 1. Desinstalar o Docker Desktop

Antes de começar, é fundamental remover o Docker Desktop para evitar conflitos de portas, serviços em segundo plano e, principalmente, conflitos de mapeamento do socket.

- Feche completamente o Docker Desktop.
- Acesse **Configurações do Windows > Aplicativos > Aplicativos instalados** e desinstale o **Docker Desktop**.
- Opcionalmente, reinicie o computador para garantir que todos os serviços e interfaces de rede virtuais tenham sido liberados.

## 2. Instalar e configurar o Podman Desktop

1. Baixe e instale o **Podman Desktop** para Windows.
2. Durante a configuração inicial, inicialize a **Podman Machine** (a máquina virtual que executará o motor) e confirme que a integração com o WSL está ativada.
3. No Podman Desktop, acesse **Settings > Preferences**.
4. Localize **Docker Socket Compatibility** e ative essa opção. Ela redireciona o socket padrão do Docker para o socket do Podman, mantendo as ferramentas de terceiros funcionando sem modificações.
5. Confirme no painel principal que o status da Podman Machine é **Running**.

## 3. Instalar `podman-compose` no WSL

Para orquestrar vários contêineres e interpretar arquivos compose, instale o `podman-compose` diretamente na distribuição Linux (WSL), usando o gerenciador de pacotes nativo.

Abra o terminal do WSL e execute:

```bash
sudo apt-get update
sudo apt-get install podman-compose
```

## 4. Configurar o VS Code

Para que a extensão *Dev Containers* use o motor do Podman e não force integrações gráficas (WSLg), que causam erros de permissão no modo *rootless*, ajuste as configurações.

Abra o arquivo `settings.json` do VS Code e adicione ou atualize estas chaves:

```json
{
  "dev.containers.dockerComposePath": "podman-compose",
  "dev.containers.dockerPath": "podman",
  "dev.containers.mountWaylandSocket": false
}
```

> **Nota de arquitetura:** `mountWaylandSocket: false` é crucial. A opção evita falhas de permissão ao tentar montar o socket Wayland do host dentro do contêiner rootless. As aplicações gráficas de depuração serão exibidas usando um servidor X (X11) executado no host Windows; portanto, o Wayland do WSLg não é necessário dentro do contêiner.

## 5. Compatibilidade dos arquivos do projeto (sem alterações)

Não é necessário alterar os arquivos do projeto para esta migração. Mantenha intactos:

- `Dockerfile`
- `docker-compose.yaml` (ou `.yml`)
- `.devcontainer/devcontainer.json`

O motor do Podman atua como substituto direto (*drop-in replacement*) e é 100% compatível com a especificação OCI. Isso permite executar o ambiente no Podman enquanto outros integrantes da equipe continuam usando Docker Desktop nos mesmos repositórios, sem conflitos.

## 6. Passo extra recomendado: criar aliases no terminal do WSL

Para facilitar o uso no dia a dia, adicione aliases ao shell para que hábitos e scripts antigos continuem funcionando:

```bash
echo "alias docker=podman" >> ~/.bashrc
echo "alias docker-compose=podman-compose" >> ~/.bashrc
source ~/.bashrc
```
