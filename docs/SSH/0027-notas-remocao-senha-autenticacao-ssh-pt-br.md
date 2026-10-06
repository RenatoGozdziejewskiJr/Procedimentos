# Notas sobre desativação da autenticação SSH por senha

[English (UK)](0027-notes-disabling-ssh-password-authentication.md)

Este procedimento explica como desativar a autenticação SSH por senha, permitindo acesso **somente** por meio de chaves SSH (o que aumenta a segurança).

> **Aviso:** Antes de prosseguir, confirme se sua chave SSH está configurada e testada. Caso contrário, você perderá o acesso ao servidor.

## 1. Conectar-se ao Raspberry Pi

Conecte-se normalmente via SSH (agora sem senha, usando sua chave):

```bash
ssh engenharia@renato-pi
```

## 2. Editar a configuração do SSH

Abra o arquivo principal de configuração do servidor SSH no Raspberry Pi com privilégios de Administrador:

```bash
sudo nano /etc/ssh/sshd_config
```

## 3. Desativar o login por senha

No arquivo, role a tela para baixo até encontrar a linha referente a `PasswordAuthentication`.

Faça o seguinte:
1. Remova o símbolo `#` no início da linha para descomentá-la e ativá-la.
2. Troque o valor `yes` por `no`.

A linha deve ficar exatamente assim:

```text
PasswordAuthentication no
```

## 4. Salvar e sair

Se estiver usando o editor `nano`:
- Pressione `Ctrl + O` para salvar o arquivo (confirme pressionando `Enter`).
- Pressione `Ctrl + X` para sair do editor.

## 5. Reiniciar o serviço SSH

Reinicie o serviço SSH para que o Raspberry Pi aplique a nova configuração de segurança:

```bash
sudo systemctl restart ssh
```
