# Notes about the Angular, Nx, Node and .NET Environment

[Português (Brasil)](0006-notas-ambiente-angular-nx-node-dotnet-pt-br.md)

## 1. Angular and Nx Workspace

### 1.1 Installation and Creation

- Install Nx globally: `npm install -g nx`
- Create a new workspace: `npx create-nx-workspace@latest`

### 1.2 Generating Components and Services

To generate elements using Nx:

```bash
# Navegar até o diretório desejado antes ou especificar o caminho
npx nx g c nome-do-componente --skipTests=true
npx nx g @nrwl/angular:service ./nome-do-servico
```

Standard Nx/Angular commands:

```bash
nx generate component nome-do-componente
nx generate service nome-do-servico
nx generate module nome-do-modulo
```

### 1.3 Running and Cleaning

- Start the project (example): `nx run bssd:serve:development`
- Clear the npm and Nx caches:
  ```bash
  npm cache clean --force
  npx nx reset
  ```

## 2. Troubleshooting Ports in Use (Windows)

Tools such as Docker or Hyper-V often reserve ports that Angular/Node tries to use (for example, 4200, 4201 and 5000).

### 2.1 Checking Which Process Is Using a Port

```cmd
netstat -ano | findstr :4201
```

To view the column headers, use `netstat -a -n -o`.

To terminate the process holding the port:

```cmd
taskkill /PID <PID> /F
```

### 2.2 Checking Ports Blocked or Excluded by the Operating System

Windows (especially with Hyper-V) reserves port ranges. To view them (Administrator privileges required):

```cmd
# Ver todas as portas TCP reservadas
netsh interface ipv4 show excludedportrange protocol=tcp

# Ver portas reservadas especificamente pelo Hyper-V
netsh interface ipv4 show dynamicportrange tcp
```

### 2.3 Reserving Ports for Development

If Hyper-V is taking development ports, you can reserve them. **Important:** stop the Docker and Hyper-V services before doing so.

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

## 3. Managing Versions (NVM and Node)

```bash
nvm list                  # Lista versões instaladas
nvm install <versao>      # Instala uma versão específica (ex: 18.16.0)
nvm use <versao>          # Usa a versão na sessão atual
nvm alias default <versao> # Define a versão padrão para novos terminais
node -v                   # Verifica a versão atual do Node
```

## 4. .NET SDK

To list the installed .NET SDKs:

```bash
dotnet --list-sdks
```
