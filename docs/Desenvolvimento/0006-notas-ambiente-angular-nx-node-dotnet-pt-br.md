# Notas sobre o ambiente Angular, Nx, Node e .NET

[English (UK)](0006-notes-angular-nx-node-dotnet.md)

## 1. Workspace Angular e Nx

### 1.1 Instalação e criação

- Instalar o Nx globalmente: `npm install -g nx`
- Criar um novo workspace: `npx create-nx-workspace@latest`

### 1.2 Geração de componentes e serviços

Para gerar elementos usando o Nx:

```bash
# Navegar até o diretório desejado antes ou especificar o caminho
npx nx g c nome-do-componente --skipTests=true
npx nx g @nrwl/angular:service ./nome-do-servico
```

Comandos padrão do Nx/Angular:

```bash
nx generate component nome-do-componente
nx generate service nome-do-servico
nx generate module nome-do-modulo
```

### 1.3 Execução e limpeza

- Iniciar o projeto (exemplo): `nx run bssd:serve:development`
- Limpar os caches do npm e do Nx:
  ```bash
  npm cache clean --force
  npx nx reset
  ```

## 2. Solução de problemas com portas em uso (Windows)

Ferramentas como Docker ou Hyper-V frequentemente reservam portas que o Angular/Node tenta usar (por exemplo, 4200, 4201 e 5000).

### 2.1 Verificar qual processo está usando uma porta

```cmd
netstat -ano | findstr :4201
```

Para ver o cabeçalho das colunas, use `netstat -a -n -o`.

Para encerrar o processo que está mantendo a porta ocupada:

```cmd
taskkill /PID <PID> /F
```

### 2.2 Verificar portas bloqueadas ou excluídas pelo sistema operacional

O Windows (especialmente com Hyper-V) reserva faixas de portas. Para visualizá-las (requer privilégios de Administrador):

```cmd
# Ver todas as portas TCP reservadas
netsh interface ipv4 show excludedportrange protocol=tcp

# Ver portas reservadas especificamente pelo Hyper-V
netsh interface ipv4 show dynamicportrange tcp
```

### 2.3 Reservar portas para desenvolvimento

Se o Hyper-V estiver ocupando as portas de desenvolvimento, é possível reservá-las. **Importante:** pare os serviços do Docker e do Hyper-V antes de fazer isso.

```cmd
# 1. Parar serviços que gerenciam portas
net stop com.docker.service
net stop winnat
net stop hns

# 2. Reservar o range (ex: 5000-5100 e 7000-7100)
netsh int ipv4 add excludedportrange protocol=tcp startport=5000 numberofports=100 store=persistent
netsh int ipv4 add excludedportrange protocol=tcp startport=7000 numberofports=100 store=persistent

# 3. Reiniciar serviços
net start winnat
net start hns
# (Inicie o Docker Desktop novamente)
```

## 3. Gerenciamento de versões (NVM e Node)

```bash
nvm list                  # Lista versões instaladas
nvm install <versao>      # Instala uma versão específica (ex: 18.16.0)
nvm use <versao>          # Usa a versão na sessão atual
nvm alias default <versao> # Define a versão padrão para novos terminais
node -v                   # Verifica a versão atual do Node
```

## 4. .NET SDK

Para listar os SDKs do .NET instalados:

```bash
dotnet --list-sdks
```
