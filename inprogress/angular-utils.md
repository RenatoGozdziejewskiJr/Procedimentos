Angular:

Instalar o nx globalmente:
npm install -g nx

Criar novo workspace:
npx create-nx-workspace@latest

Criar novo componente:
no diretório de componentes, criar pasta com o nome do componente
criar componente com nx: npx nx g c sub-header-working-mode --skipTests=true
criar service com nx : npx nx g @nrwl/angular:service ./calibration-service 
nx generate component nome-do-componente
nx generate service nome-do-servico
nx generate module nome-do-modulo

para inciar o processo: nx run bssd:serve:development

Limpar o cache:

npm cache clean --force
npx nx reset 


--- Problemas com portas em uso:

1) Verificar se alguma porta está em uso: netstat -ano | findstr :4201
para ver o cabecalho: netstat -a -n -o
para matar o processo: taskkill /PID <PID> /F

2) Verificar portas que estão excluidas/bloqueadas pelo SO (*admim):

# Ver todas as portas TCP reservadas
netsh interface ipv4 show excludedportrange protocol=tcp

# Ver portas reservadas pelo Hyper-V especificamente
netsh interface ipv4 show dynamicportrange tcp

4) Parar serviços:
# Parar o Docker
net stop com.docker.service
# ou pelo Docker Desktop: botão direito no ícone > Quit Docker Desktop

# Parar o WinNAT (componente que reserva portas)
net stop winnat

# Parar o Hyper-V Host Compute Service
net stop hns

# Reiniciar o computador (recomendado)
# Ou reiniciar os serviços:
net start winnat
net start hns
# Iniciar Docker novamente
 
3) Reservar Portas para Dev - IMPORTANTE: Com o Docker/Hyper-V parados, depois reinicie-os.
# Reservar range 5000-5100 para desenvolvimento (não deixar Hyper-V pegar)
netsh int ipv4 add excludedportrange protocol=tcp startport=5000 numberofports=100 store=persistent

# Reservar range 7000-7100 (alternativa)
netsh int ipv4 add excludedportrange protocol=tcp startport=7000 numberofports=100 store=persistent

# Ver o que foi reservado
netsh int ipv4 show excludedportrange protocol=tcp


-----
versoes do node...
nvm list

nvm install x.x.x
nvm alias default x.x.x ou nvm use x.x.x 

node -v (verifica a versao do node)
 
----
versoes do dotnet
dotnet --list-sdks