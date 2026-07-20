# Remoção de Senha na Autenticação SSH

Este procedimento explica como desativar a autenticação por senha no SSH, permitindo acesso **apenas** através de chaves SSH (aumentando a segurança).

> **Aviso:** Antes de prosseguir, certifique-se de que a sua chave SSH está configurada e testada. Caso contrário, você perderá o acesso ao servidor!

## 1. Acessar o Raspberry Pi

Conecte-se normalmente via SSH (agora sem senha, utilizando a sua chave):

```bash
ssh engenharia@renato-pi
```

## 2. Editar a configuração do SSH

Abra o arquivo principal de configuração do servidor SSH no seu Raspberry Pi com privilégios de administrador:

```bash
sudo nano /etc/ssh/sshd_config
```

## 3. Desativar o login por senhas

Dentro do arquivo, role a tela para baixo até encontrar a linha referente a `PasswordAuthentication`.

Faça duas coisas:
1. Apague o símbolo `#` no começo da linha (para descomentá-la e ativá-la).
2. Troque o valor `yes` por `no`.

A linha deve ficar exatamente assim:

```text
PasswordAuthentication no
```

## 4. Salvar e sair

Se estiver utilizando o editor `nano`:
- Pressione `Ctrl + O` para salvar o arquivo (confirme com a tecla `Enter`).
- Pressione `Ctrl + X` para sair do editor.

## 5. Reiniciar o serviço SSH

Para que o Raspberry Pi aplique a nova regra de segurança, você precisa reiniciar o serviço do SSH:

```bash
sudo systemctl restart ssh
```