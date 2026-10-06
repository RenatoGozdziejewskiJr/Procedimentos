# Notas sobre liberação de uma porta reservada no Windows

[English (UK)](0024-notes-windows-reserved-ports.md)

## 1. Liberar a porta no Windows

Se o seu programa precisar obrigatoriamente usar a porta 50713, reiniciar o WinNAT pode fazer com que o Windows atribua outras faixas de portas excluídas. Isso não garante a liberação de uma porta específica e pode interromper serviços que dependem de NAT.

### 1.1 Abrir o Prompt de Comando como Administrador

Abra o menu Iniciar, digite `cmd`, clique com o botão direito e selecione **Executar como Administrador**.

### 1.2 Parar o serviço de rede NAT

Digite o seguinte comando e pressione Enter:

`net stop winnat`

### 1.3 Iniciar o serviço novamente

Inicie o serviço novamente digitando:

`net start winnat`

### 1.4 Abrir o programa

Verifique as faixas de portas TCP excluídas no momento:

```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

Confirme que a porta 50713 não está dentro de uma faixa excluída e verifique se o programa consegue vinculá-la e usá-la. Se ela continuar indisponível, use outra porta em vez de presumir que a reinicialização a liberou.
