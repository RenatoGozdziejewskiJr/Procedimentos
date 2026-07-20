# Utilitários de Desenvolvimento (Angular, Nx, Node, .NET)

## Angular & Nx Workspace

### Instalação e Criação
- Instalar o Nx globalmente: `npm install -g nx`
- Criar novo workspace: `npx create-nx-workspace@latest`

### Geração de Componentes e Serviços
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

### Execução e Limpeza
- Iniciar o projeto (exemplo): `nx run bssd:serve:development`
- Limpar o cache do npm e do Nx:
  ```bash
  npm cache clean --force
  npx nx reset 
  ```

---

## Resolução de Problemas com Portas em Uso (Windows)

Muitas vezes, ferramentas como Docker ou Hyper-V reservam portas que o Angular/Node tenta usar (ex: 4200, 4201, 5000).

### 1. Verificar quem está usando a porta
```cmd
netstat -ano | findstr :4201
```
*(Para ver o cabeçalho das colunas, use `netstat -a -n -o`)*

Para matar o processo que está segurando a porta:
```cmd
taskkill /PID <PID> /F
```

### 2. Verificar portas bloqueadas/excluídas pelo SO
O Windows (especialmente com Hyper-V) reserva faixas de portas. Para ver essas faixas (requer Admin):
```cmd
# Ver todas as portas TCP reservadas
netsh interface ipv4 show excludedportrange protocol=tcp

# Ver portas reservadas especificamente pelo Hyper-V
netsh interface ipv4 show dynamicportrange tcp
```

### 3. Solução: Reservar portas para Desenvolvimento
Se o Hyper-V estiver "roubando" suas portas de dev, você pode reservá-las. **Importante:** Faça isso com os serviços do Docker e Hyper-V parados.

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

---

## Gerenciamento de Versões (NVM e Node)

```bash
nvm list                  # Lista versões instaladas
nvm install <versao>      # Instala uma versão específica (ex: 18.16.0)
nvm use <versao>          # Usa a versão na sessão atual
nvm alias default <versao> # Define a versão padrão para novos terminais
node -v                   # Verifica a versão atual do Node
```

## .NET SDK
Para listar os SDKs instalados do .NET:
```bash
dotnet --list-sdks
```
