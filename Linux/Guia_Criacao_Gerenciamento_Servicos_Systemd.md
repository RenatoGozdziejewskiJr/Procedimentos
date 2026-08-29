# Guia Prático: Criação e Gerenciamento de Serviços no Linux com Systemd (systemctl)

Este guia foi elaborado para iniciantes e explica de forma didática como criar, configurar e gerenciar serviços de inicialização automática no Linux utilizando o **systemd** e o utilitário **systemctl**.

---

## 1. O que é o Systemd e o Systemctl?

- **systemd:** É o sistema de inicialização e gerenciador de serviços padrão na maioria das distribuições Linux modernas (Debian, Ubuntu, CentOS, Fedora, Arch, Radxa OS, Raspberry Pi OS). Ele é o primeiro processo a ser executado (`PID 1`) e funciona como o "maestro" do sistema operacional, controlando o que inicia, para ou reinicia.
- **systemctl:** É o comando de terminal que usamos para interagir e dar ordens ao `systemd` (iniciar, parar, habilitar no boot, ver logs, etc.).

---

## 2. A Anatomia de um Arquivo de Serviço (`.service`)

Os arquivos de serviço do sistema são salvos no diretório:
```text
/etc/systemd/system/nome-do-servico.service
```

Um arquivo `.service` é dividido em três blocos principais (`[Unit]`, `[Service]` e `[Install]`):

```ini
[Unit]
Description=Meu Servico Personalizado
After=network.target

[Service]
Type=simple
User=radxa
WorkingDirectory=/home/radxa/meu-projeto
ExecStart=/usr/bin/python3 /home/radxa/meu-projeto/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### O que significa cada seção:

#### `[Unit]` (Metadados e Dependências)
- **`Description=`**: Descrição legível do serviço que aparece nos logs e no comando de status.
- **`After=`**: Define o que precisa estar pronto antes deste serviço iniciar. Exemplo: `network.target` (espera a rede estar ativa).

#### `[Service]` (Como o programa deve rodar)
- **`Type=`**:
  - `simple` (padrão): Para processos que rodam continuamente em primeiro plano no terminal (ex.: servidores web, scripts em loop, bots).
  - `forking`: Para programas que iniciam e criam um processo filho em background (ex.: TigerVNC, Nginx clássico).
  - `oneshot`: Para tarefas que executam um comando rápido, terminam e não precisam ficar rodando (ex.: scripts de backup ou limpeza).
- **`User=` e `Group=`**: Define o usuário Linux que executará o comando (evite rodar como `root` a menos que seja estritamente necessário).
- **`WorkingDirectory=`**: A pasta onde o comando deve ser executado (equivalente a dar um `cd` antes).
- **`ExecStart=`**: O comando exato que inicia o programa. **Importante:** Sempre use o caminho absoluto dos executáveis (ex.: `/usr/bin/python3` em vez de apenas `python3`).
- **`Restart=`**:
  - `always`: Se o programa cair ou fechar inesperadamente, o systemd reinicia ele automaticamente.
  - `on-failure`: Só reinicia se o programa fechar com código de erro.
- **`RestartSec=`**: Tempo em segundos para aguardar antes de tentar reiniciar.

#### `[Install]` (Como o serviço é ativado no boot)
- **`WantedBy=multi-user.target`**: Informa que o serviço deve ser iniciado no modo padrão de operação do sistema (modo texto/gráfico com rede).

---

## 3. Passo a Passo: Criando um Serviço do Zero

Vamos criar um exemplo prático de um script que grava a data e hora em um arquivo a cada 10 segundos.

### Passo 1: Criar o Script
Crie um script em `/home/radxa/meu_script.sh`:

```bash
#!/bin/bash
while true; do
    echo "Servico rodando em: $(date)" >> /home/radxa/servico.log
    sleep 10
done
```

Dê permissão de execução:
```bash
chmod +x /home/radxa/meu_script.sh
```

### Passo 2: Criar o Arquivo de Serviço no Systemd
Abra o editor `nano` com permissão de superusuário:

```bash
sudo nano /etc/systemd/system/meu-script.service
```

Cole o conteúdo:

```ini
[Unit]
Description=Script de Exemplo para Aprendizado
After=network.target

[Service]
Type=simple
User=radxa
ExecStart=/bin/bash /home/radxa/meu_script.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
Salve (`Ctrl + O`, `Enter`) e saia (`Ctrl + X`).

### Passo 3: Recarregar o Systemd
Sempre que criar ou modificar qualquer arquivo `.service`, é **obrigatório** avisar o systemd:

```bash
sudo systemctl daemon-reload
```

### Passo 4: Iniciar e Habilitar no Boot
- **Iniciar imediatamente:**
  ```bash
  sudo systemctl start meu-script.service
  ```
- **Habilitar para subir sozinho quando a placa ligar:**
  ```bash
  sudo systemctl enable meu-script.service
  ```
- *(Dica: Você pode juntar os dois comandos com `sudo systemctl enable --now meu-script.service`)*

---

## 4. O que é o Símbolo `@` nos Serviços (Serviços Template)?

Você já deve ter visto serviços com `@`, como `tigervncserver@:1.service` ou `openvpn@client.service`.

- O `@` indica que o arquivo é um **modelo (template)**.
- O arquivo no disco se chama `tigervncserver@.service`.
- O valor colocado depois do `@` (como `:1` ou `meu-cliente`) é passado para dentro do serviço como a variável **`%i`** ou **`%I`**.
- **Benefício:** Permite criar instâncias dinâmicas sem duplicar arquivos de serviço. Por exemplo:
  - `tigervncserver@:1.service` roda para o display `:1`.
  - `tigervncserver@:2.service` roda para o display `:2`.

---

## 5. Tabela de Comandos Essenciais do `systemctl`

| Ação | Comando | Descrição |
| :--- | :--- | :--- |
| **Recarregar definições** | `sudo systemctl daemon-reload` | Recarrega arquivos `.service` novos ou alterados |
| **Iniciar** | `sudo systemctl start nome.service` | Inicia o serviço agora |
| **Parar** | `sudo systemctl stop nome.service` | Para a execução do serviço |
| **Reiniciar** | `sudo systemctl restart nome.service` | Para e inicia o serviço novamente |
| **Ver Status** | `sudo systemctl status nome.service` | Mostra se está rodando (`active`), PID e últimos logs |
| **Habilitar no Boot** | `sudo systemctl enable nome.service` | Faz o serviço iniciar automaticamente ao ligar |
| **Desabilitar do Boot** | `sudo systemctl disable nome.service` | Remove o serviço da inicialização automática |
| **Habilitar e Iniciar** | `sudo systemctl enable --now nome.service` | Faz as duas ações em um único comando |
| **Verificar se está ativo** | `systemctl is-active nome.service` | Retorna `active` ou `inactive` (ótimo para scripts) |
| **Verificar se inicia no boot**| `systemctl is-enabled nome.service` | Retorna `enabled` ou `disabled` |

---

## 6. Como Diagnosticar Problemas e Ver Logs (`journalctl`)

Quando um serviço falha ao iniciar (`Active: failed`), o comando `journalctl` é a melhor ferramenta para entender o que deu errado:

- **Ver os logs do serviço em tempo real:**
  ```bash
  journalctl -u nome.service -f
  ```
- **Ver as últimas linhas de log sem paginação:**
  ```bash
  journalctl -u nome.service -e --no-pager
  ```
- **Ver os logs apenas do boot atual:**
  ```bash
  journalctl -u nome.service -b
  ```

---

## 7. Boas Práticas e Cuidados Importantes

1. **Caminhos Absolutos:** No `ExecStart=`, nunca use comandos relativos como `python main.py`. Use `/usr/bin/python3 /home/usuario/main.py`. Descubra o caminho de um executável com `which python3` ou `which node`.
2. **Permissões de Arquivo:** Certifique-se de que o usuário declarado em `User=` tem permissão de leitura e execução nos scripts e pastas referenciadas.
3. **Loop Infinito de Quedas:** Ao usar `Restart=always`, use sempre um `RestartSec=5` para evitar que o systemd tente reiniciar o programa centenas de vezes por segundo caso haja um erro fatal de sintaxe no código.
