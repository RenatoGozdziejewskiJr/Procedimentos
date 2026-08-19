### Liberar a porta no Windows
Se o seu programa obrigatoriamente precisa rodar na porta 50713, você pode forçar o Windows a embaralhar essas reservas reiniciando o serviço de rede responsável por elas (o WinNAT).

**1.Abra o Prompt de Comando como Administrador:**

Clique no menu Iniciar, digite `cmd`, clique com o botão direito e selecione **Executar como Administrador**.

**2.Pare o serviço de rede NAT:**

Digite o seguinte comando e aperte Enter:

`net stop winnat`

**3.Inicie o serviço novamente:**Neste momento, a porta 50713 foi liberada..

Agora, religue o serviço digitando:

`net start winnat`

**4.Abra o seu programa:**

Quando o serviço WinNAT reinicia, ele geralmente escolhe blocos de portas diferentes. Tente conectar o seu programa novamente (ou rodar o script do PowerShell).