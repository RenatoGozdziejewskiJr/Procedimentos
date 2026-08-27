# Guia de Migração: Docker Desktop para Podman (com VS Code Dev Containers e WSL 2)

Este guia documenta o passo a passo para substituir o Docker Desktop pelo Podman Desktop no Windows, mantendo total compatibilidade com o uso de Dev Containers no VS Code através do WSL 2.

## 1. Desinstalar o Docker Desktop
Antes de iniciar, é fundamental remover o Docker Desktop para evitar conflitos de portas, serviços em segundo plano e, principalmente, conflitos de mapeamento do socket.
* Feche o Docker Desktop completamente.
* Vá em **Configurações do Windows > Aplicativos > Aplicativos Instalados** e desinstale o **Docker Desktop**.
* (Opcional) Reinicie o computador para garantir que todos os serviços e interfaces de rede virtuais foram liberados.

## 2. Instalar e Configurar o Podman Desktop
1. Baixe e instale o **Podman Desktop** para Windows.
2. Durante o *setup* inicial, inicialize a **Podman Machine** (a máquina virtual que rodará o motor por baixo) e garanta que a integração com o WSL esteja ativada.
3. No Podman Desktop, vá em **Settings > Preferences**.
4. Procure por **Docker Socket Compatibility** e ative essa opção. Isso cria um redirecionamento do socket padrão do Docker para o do Podman, mantendo ferramentas de terceiros funcionando sem modificações.
5. Certifique-se de que a Podman Machine está com o status **Running** no painel principal.

## 3. Instalar o `podman-compose` no WSL
Para orquestrar múltiplos contêineres e interpretar os arquivos compose, instale o `podman-compose` diretamente na sua distribuição Linux (WSL). Utilizaremos o gerenciador de pacotes nativo:

Abra o terminal do seu WSL e execute:
```bash
sudo apt-get update
sudo apt-get install podman-compose
```

## 4. Configurar o VS Code
Para que a extensão *Dev Containers* utilize o motor do Podman e não tente forçar integrações gráficas (WSLg) que causam erros de permissão no modo *rootless*, precisamos ajustar as configurações.

Abra o arquivo `settings.json` do VS Code e adicione/atualize as seguintes chaves:
```json
{
  "dev.containers.dockerComposePath": "podman-compose",
  "dev.containers.dockerPath": "podman",
  "dev.containers.mountWaylandSocket": false
}
```
> **Nota de Arquitetura:** A opção `mountWaylandSocket: false` é crucial. Ela evita falhas de permissão ao tentar montar o socket Wayland do host para dentro do contêiner rootless. Como as aplicações gráficas para debug serão exibidas utilizando um servidor X (X11) rodando no host Windows, o Wayland do WSLg não é necessário dentro do contêiner.

## 5. Compatibilidade dos Arquivos de Projeto (Zero Alterações)
A melhor parte dessa migração é que **não é necessário fazer nenhuma alteração** nos arquivos do seu projeto. Você pode e deve manter intactos:
* `Dockerfile`
* `docker-compose.yaml` (ou `.yml`)
* `.devcontainer/devcontainer.json`

O motor do Podman atua como um substituto direto (*drop-in replacement*) e é 100% compatível com a especificação OCI. Isso garante que o seu ambiente rode perfeitamente no Podman enquanto outros membros da equipe podem continuar utilizando o Docker Desktop nos mesmos repositórios sem conflitos.

## Passo Extra Recomendado: Criar Aliases no Terminal do WSL
Para facilitar o uso no dia a dia, adicione aliases no seu shell para que seus costumes e scripts antigos funcionem naturalmente:
```bash
echo "alias docker=podman" >> ~/.bashrc
echo "alias docker-compose=podman-compose" >> ~/.bashrc
source ~/.bashrc
```
